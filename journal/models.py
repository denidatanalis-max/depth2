from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Role(models.TextChoices):
    SUPERVISOR = 'supervisor', 'Writer (Penulis)'
    MANAGER = 'manager', 'Leader (Approver)'
    ADMIN = 'admin', 'Admin (Helpdesk)'
    SCORING = 'scoring', 'Scoring (Penilai)'
    RECOMMENDATION = 'recommendation', 'Recommendation (Tim Rekomendasi)'
    SUPERADMIN = 'superadmin', 'Super Admin'


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervisors',
        limit_choices_to={'role': Role.MANAGER},
        help_text='Atasan langsung (hanya untuk Writer)',
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
    def is_recommendation(self):
        return self.role == Role.RECOMMENDATION

    @property
    def is_superadmin(self):
        return self.role == Role.SUPERADMIN


class JournalStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Diajukan ke Leader'
    APPROVED = 'approved', 'Disetujui Leader'
    REJECTED = 'rejected', 'Ditolak Leader'
    UPLOADED = 'uploaded', 'Menunggu Review File Leader'
    UNDER_REVIEW = 'under_review', 'Dikumpulkan Admin'
    REVISION_NEEDED = 'revision_needed', 'Perlu Revisi'
    VERIFIED = 'verified', 'Diverifikasi Admin'
    SCORING = 'scoring', 'Sedang Dinilai'
    SCORE_REVISION = 'score_revision', 'Revisi dari Scoring'
    UNDER_RECOMMENDATION = 'under_recommendation', 'Menunggu Tim Rekomendasi'
    RECOMMENDED = 'recommended', 'Direkomendasikan'
    NOT_RECOMMENDED = 'not_recommended', 'Tidak Direkomendasikan'
    PUBLISHED = 'published', 'Dipublikasikan'


class Journal(models.Model):
    title = models.CharField('Judul Jurnal', max_length=500)
    abstract = models.TextField('ringkasan', blank=True)
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
    abstract_updated_at = models.DateTimeField('Ringkasan Terakhir Diubah', null=True, blank=True)
    published_at = models.DateTimeField('Tanggal Publikasi', null=True, blank=True)
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
            JournalStatus.SCORING: 'warning',
            JournalStatus.SCORE_REVISION: 'danger',
            JournalStatus.UNDER_RECOMMENDATION: 'warning',
            JournalStatus.RECOMMENDED: 'success',
            JournalStatus.NOT_RECOMMENDED: 'danger',
            JournalStatus.PUBLISHED: 'dark',
        }
        return mapping.get(self.status, 'secondary')

    @property
    def latest_score(self):
        return self.scores.order_by('-created_at').first()


class JournalScore(models.Model):
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        related_name='scores',
    )
    scorer = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': Role.SCORING},
    )
    writing_clarity = models.PositiveIntegerField(
        'Kejelasan Penulisan (0-100)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    problem_clarity = models.PositiveIntegerField(
        'Identifikasi Masalah (0-100)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    solution_quality = models.PositiveIntegerField(
        'Kualitas Solusi (0-100)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    positive_impact = models.PositiveIntegerField(
        'Dampak Positif (0-100)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    risk_awareness = models.PositiveIntegerField(
        'Identifikasi Risiko (0-100)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    note = models.TextField('Catatan Penilai', blank=True)

    class Recommendation(models.TextChoices):
        RECOMMEND = 'recommend', 'Layak Dipublikasikan'
        REVISION = 'revision', 'Perlu Revisi'
        REJECT = 'reject', 'Tidak Layak'

    recommendation = models.CharField(
        'Rekomendasi',
        max_length=20,
        choices=Recommendation.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Skor {self.journal.title} — {self.total_score}/500'

    @property
    def total_score(self):
        return self.writing_clarity + self.problem_clarity + self.solution_quality + self.positive_impact + self.risk_awareness

    @property
    def average_score(self):
        return self.total_score / 5


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
