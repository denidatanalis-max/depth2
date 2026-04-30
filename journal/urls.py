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

    # Manager — review judul/ringkasan
    path('journal/<int:pk>/approve/', views.manager_approve, name='manager_approve'),
    path('journal/<int:pk>/reject/', views.manager_reject, name='manager_reject'),
    # Manager — review file PDF
    path('journal/<int:pk>/approve-file/', views.manager_approve_file, name='manager_approve_file'),
    path('journal/<int:pk>/reject-file/', views.manager_reject_file, name='manager_reject_file'),

    # Admin
    path('journal/<int:pk>/collect/', views.admin_collect, name='admin_collect'),

    # Scoring
    path('journal/<int:pk>/score/', views.scoring_submit, name='scoring_submit'),

    # Recommendation
    path('journal/<int:pk>/recommend-approve/', views.recommendation_approve, name='recommendation_approve'),
    path('journal/<int:pk>/recommend-reject/', views.recommendation_reject, name='recommendation_reject'),

    # Publication
    path('journal/<int:pk>/publish/', views.publish_journal, name='publish_journal'),
]
