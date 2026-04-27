from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Journal, JournalLog, JournalStatus, Role, UserProfile
from .forms import JournalCreateForm, JournalUploadForm, ReviewForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Username atau password salah.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def get_profile(user):
    return UserProfile.objects.get(user=user)


@login_required
def dashboard(request):
    profile = get_profile(request.user)

    if profile.is_supervisor:
        journals = Journal.objects.filter(author=profile)
        return render(request, 'dashboard/supervisor.html', {
            'profile': profile,
            'journals': journals,
        })

    elif profile.is_manager:
        supervisor_profiles = UserProfile.objects.filter(manager=profile)
        pending = Journal.objects.filter(
            author__in=supervisor_profiles,
            status=JournalStatus.SUBMITTED,
        )
        all_journals = Journal.objects.filter(
            author__in=supervisor_profiles,
        ).exclude(status=JournalStatus.DRAFT)
        return render(request, 'dashboard/manager.html', {
            'profile': profile,
            'pending': pending,
            'all_journals': all_journals,
            'supervisor_count': supervisor_profiles.count(),
        })

    elif profile.is_admin:
        uploaded = Journal.objects.filter(status=JournalStatus.UPLOADED)
        under_review = Journal.objects.filter(status=JournalStatus.UNDER_REVIEW)
        all_journals = Journal.objects.exclude(status=JournalStatus.DRAFT)
        return render(request, 'dashboard/admin.html', {
            'profile': profile,
            'uploaded': uploaded,
            'under_review': under_review,
            'all_journals': all_journals,
        })

    elif profile.is_superadmin:
        all_journals = Journal.objects.all()
        all_users = UserProfile.objects.all()
        return render(request, 'dashboard/superadmin.html', {
            'profile': profile,
            'all_journals': all_journals,
            'all_users': all_users,
        })

    return render(request, 'dashboard/default.html', {'profile': profile})


# --- Supervisor views ---

@login_required
def journal_create(request):
    profile = get_profile(request.user)
    if not profile.is_supervisor:
        return HttpResponseForbidden('Hanya Supervisor yang bisa membuat jurnal.')

    if request.method == 'POST':
        form = JournalCreateForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.author = profile
            journal.save()
            JournalLog.objects.create(
                journal=journal, action='Dibuat', by_user=profile,
                note='Jurnal baru dibuat sebagai draft.',
            )
            messages.success(request, 'Jurnal berhasil dibuat sebagai draft.')
            return redirect('journal_detail', pk=journal.pk)
    else:
        form = JournalCreateForm()
    return render(request, 'journal/create.html', {'form': form, 'profile': profile})


@login_required
def journal_detail(request, pk):
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    # Access control
    if profile.is_supervisor and journal.author != profile:
        return HttpResponseForbidden('Anda tidak memiliki akses ke jurnal ini.')
    if profile.is_manager:
        if journal.author.manager != profile:
            return HttpResponseForbidden('Jurnal ini bukan milik supervisor Anda.')

    logs = journal.logs.all()
    upload_form = JournalUploadForm(instance=journal)
    review_form = ReviewForm()

    return render(request, 'journal/detail.html', {
        'journal': journal,
        'profile': profile,
        'logs': logs,
        'upload_form': upload_form,
        'review_form': review_form,
    })


@login_required
def journal_edit(request, pk):
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_supervisor or journal.author != profile:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status not in (JournalStatus.DRAFT, JournalStatus.REJECTED, JournalStatus.REVISION_NEEDED):
        messages.error(request, 'Jurnal tidak bisa diedit pada status ini.')
        return redirect('journal_detail', pk=pk)

    if request.method == 'POST':
        form = JournalCreateForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            JournalLog.objects.create(
                journal=journal, action='Diedit', by_user=profile,
                note='Jurnal diedit oleh penulis.',
            )
            messages.success(request, 'Jurnal berhasil diperbarui.')
            return redirect('journal_detail', pk=pk)
    else:
        form = JournalCreateForm(instance=journal)
    return render(request, 'journal/edit.html', {
        'form': form, 'journal': journal, 'profile': profile,
    })


@login_required
def journal_submit(request, pk):
    """Step 02: Supervisor submits journal to Manager for approval."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_supervisor or journal.author != profile:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status not in (JournalStatus.DRAFT, JournalStatus.REJECTED, JournalStatus.REVISION_NEEDED):
        messages.error(request, 'Jurnal tidak bisa diajukan pada status ini.')
        return redirect('journal_detail', pk=pk)
    if not profile.manager:
        messages.error(request, 'Anda belum memiliki manager. Hubungi admin.')
        return redirect('journal_detail', pk=pk)

    journal.status = JournalStatus.SUBMITTED
    journal.save()
    JournalLog.objects.create(
        journal=journal, action='Diajukan', by_user=profile,
        note=f'Diajukan ke Manager: {profile.manager.user.get_full_name()}',
    )
    messages.success(request, 'Jurnal berhasil diajukan ke Manager untuk persetujuan.')
    return redirect('journal_detail', pk=pk)


@login_required
def journal_upload(request, pk):
    """Step 03: Supervisor uploads the journal file after Manager approval."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_supervisor or journal.author != profile:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status != JournalStatus.APPROVED:
        messages.error(request, 'Jurnal hanya bisa diupload setelah disetujui Manager.')
        return redirect('journal_detail', pk=pk)

    if request.method == 'POST':
        form = JournalUploadForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.status = JournalStatus.UPLOADED
            journal.save()
            JournalLog.objects.create(
                journal=journal, action='File Diupload', by_user=profile,
                note=f'File jurnal diupload: {journal.file.name}',
            )
            messages.success(request, 'File jurnal berhasil diupload. Menunggu verifikasi Admin.')
            return redirect('journal_detail', pk=pk)
    else:
        form = JournalUploadForm(instance=journal)
    return render(request, 'journal/upload.html', {
        'form': form, 'journal': journal, 'profile': profile,
    })


# --- Manager views ---

@login_required
def manager_approve(request, pk):
    """Step 02: Manager approves the journal."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_manager or journal.author.manager != profile:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status != JournalStatus.SUBMITTED:
        messages.error(request, 'Jurnal tidak dalam status menunggu persetujuan.')
        return redirect('journal_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        note = form.cleaned_data.get('note', '') if form.is_valid() else ''
        journal.status = JournalStatus.APPROVED
        journal.save()
        JournalLog.objects.create(
            journal=journal, action='Disetujui Manager', by_user=profile,
            note=note or 'Jurnal disetujui oleh Manager.',
        )
        messages.success(request, 'Jurnal berhasil disetujui.')
    return redirect('journal_detail', pk=pk)


@login_required
def manager_reject(request, pk):
    """Step 02: Manager rejects the journal (back to supervisor for revision)."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_manager or journal.author.manager != profile:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status != JournalStatus.SUBMITTED:
        messages.error(request, 'Jurnal tidak dalam status menunggu persetujuan.')
        return redirect('journal_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        note = form.cleaned_data.get('note', '') if form.is_valid() else ''
        journal.status = JournalStatus.REJECTED
        journal.revision_count += 1
        journal.save()
        JournalLog.objects.create(
            journal=journal, action='Ditolak Manager', by_user=profile,
            note=note or 'Jurnal ditolak, perlu revisi.',
        )
        messages.warning(request, 'Jurnal ditolak dan dikembalikan ke Supervisor untuk revisi.')
    return redirect('journal_detail', pk=pk)


# --- Admin views ---

@login_required
def admin_start_review(request, pk):
    """Step 04/05: Admin starts reviewing the uploaded journal."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_admin:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status != JournalStatus.UPLOADED:
        messages.error(request, 'Jurnal tidak dalam status siap diverifikasi.')
        return redirect('journal_detail', pk=pk)

    journal.status = JournalStatus.UNDER_REVIEW
    journal.save()
    JournalLog.objects.create(
        journal=journal, action='Mulai Verifikasi', by_user=profile,
        note='Admin mulai memverifikasi jurnal.',
    )
    messages.info(request, 'Jurnal sedang diverifikasi.')
    return redirect('journal_detail', pk=pk)


@login_required
def admin_verify(request, pk):
    """Step 05: Admin verifies the journal - passes to next stage."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_admin:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status != JournalStatus.UNDER_REVIEW:
        messages.error(request, 'Jurnal tidak dalam status sedang diverifikasi.')
        return redirect('journal_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        note = form.cleaned_data.get('note', '') if form.is_valid() else ''
        journal.status = JournalStatus.VERIFIED
        journal.save()
        JournalLog.objects.create(
            journal=journal, action='Diverifikasi Admin', by_user=profile,
            note=note or 'Jurnal lolos verifikasi admin.',
        )
        messages.success(request, 'Jurnal diverifikasi dan siap untuk tahap selanjutnya.')
    return redirect('journal_detail', pk=pk)


@login_required
def admin_request_revision(request, pk):
    """Step 04 loop: Admin sends journal back for revision."""
    profile = get_profile(request.user)
    journal = get_object_or_404(Journal, pk=pk)

    if not profile.is_admin:
        return HttpResponseForbidden('Tidak diizinkan.')
    if journal.status not in (JournalStatus.UPLOADED, JournalStatus.UNDER_REVIEW):
        messages.error(request, 'Jurnal tidak bisa dikembalikan pada status ini.')
        return redirect('journal_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        note = form.cleaned_data.get('note', '') if form.is_valid() else ''
        journal.status = JournalStatus.REVISION_NEEDED
        journal.revision_count += 1
        journal.save()
        JournalLog.objects.create(
            journal=journal, action='Perlu Revisi', by_user=profile,
            note=note or 'Jurnal dikembalikan untuk revisi.',
        )
        messages.warning(request, 'Jurnal dikembalikan ke Supervisor untuk revisi.')
    return redirect('journal_detail', pk=pk)
