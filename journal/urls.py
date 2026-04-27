from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Public (no login)
    path('publikasi/', views.public_journals, name='public_journals'),
    path('publikasi/<int:pk>/', views.public_journal_detail, name='public_journal_detail'),

    # Supervisor
    path('journal/create/', views.journal_create, name='journal_create'),
    path('journal/<int:pk>/', views.journal_detail, name='journal_detail'),
    path('journal/<int:pk>/edit/', views.journal_edit, name='journal_edit'),
    path('journal/<int:pk>/submit/', views.journal_submit, name='journal_submit'),
    path('journal/<int:pk>/upload/', views.journal_upload, name='journal_upload'),

    # Manager
    path('journal/<int:pk>/approve/', views.manager_approve, name='manager_approve'),
    path('journal/<int:pk>/reject/', views.manager_reject, name='manager_reject'),

    # Admin
    path('journal/<int:pk>/start-review/', views.admin_start_review, name='admin_start_review'),
    path('journal/<int:pk>/verify/', views.admin_verify, name='admin_verify'),
    path('journal/<int:pk>/request-revision/', views.admin_request_revision, name='admin_request_revision'),

    # Scoring
    path('journal/<int:pk>/score/', views.scoring_submit, name='scoring_submit'),

    # Publication
    path('journal/<int:pk>/publish/', views.publish_journal, name='publish_journal'),
]
