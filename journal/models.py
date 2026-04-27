from django.db import models
from django.conf import settings
from django.utils import timezone


class Role(models.TextChoices):
    SUPERVISOR = 'supervisor', 'Supervisor (Penulis)'
    MANAGER = 'manager', 'Manager (Approver)'
    ADMIN = 'admin', 'Admin (Helpdesk)'
    SCORING = 'scoring', 'Scoring (Penilai)'
    SUPERADMIN = 'superadmin', 'Super Admin'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervisors',
        limit_choices_to={'role': Role.MANAGER},
        help_text='Atasan langsung (hanya untuk Supervisor)',
    )

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.get_role_display()})'

    @property
    def is_supervisor(self):
        return self.role == Role.SUPERVISOR

    @property
    def is_manager(self):
        return self.role == Role.MANAGER

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_scoring(self):
        return self.role == Role.SCORING

    @property
    def is_superadmin(self):
        return self.role == Role.SUPERADMIN


class JournalStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Diajukan ke Manager'
    APPROVED = 'approved', 'Disetujui Manager'
    REJECTED = 'rejected', 'Ditolak Manager'
    UPLOADED = 'uploaded', 'Jurnal Diupload'
    UNDER_REVIEW = 'under_review', 'Sedang Diverifikasi Admin'
    REVISION_NEEDED = 'revision_needed', 'Perlu Revisi'
    VERIFIED = 'verified', 'Diverifikasi Admin'
    READY_SCORING = 'ready_scoring', 'Siap Dinilai'


class Journal(models.Model):
    title = models.CharField('Judul Jurnal', max_length=500)
    abstract = models.TextField('Abstrak', blank=True)
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='journals',
        limit_choices_to={'role': Role.SUPERVISOR},
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=JournalStatus.choices,
        default=JournalStatus.DRAFT,
    )
    file = models.FileField(
        'File Jurnal (PDF)',
        upload_to='journals/%Y/%m/',
        blank=True,
        null=True,
    )
    revision_count = models.PositiveIntegerField('Jumlah Revisi', default=0)
    created_at = models.DateTimeField('Dibuat', auto_now_add=True)
    updated_at = models.DateTimeField('Diperbarui', auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Jurnal'
        verbose_name_plural = 'Jurnal'

    def __str__(self):
        return f'{self.title} — {self.author.user.get_full_name()}'

    @property
    def status_badge_class(self):
        mapping = {
            JournalStatus.DRAFT: 'secondary',
            JournalStatus.SUBMITTED: 'primary',
            JournalStatus.APPROVED: 'info',
            JournalStatus.REJECTED: 'danger',
            JournalStatus.UPLOADED: 'info',
            JournalStatus.UNDER_REVIEW: 'warning',
            JournalStatus.REVISION_NEEDED: 'danger',
            JournalStatus.VERIFIED: 'success',
            JournalStatus.READY_SCORING: 'success',
        }
        return mapping.get(self.status, 'secondary')


class JournalLog(models.Model):
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        related_name='logs',
    )
    action = models.CharField('Aksi', max_length=50)
    by_user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
    )
    note = models.TextField('Catatan', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.journal.title} — {self.action} oleh {self.by_user}'
