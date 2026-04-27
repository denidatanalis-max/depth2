from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from journal.models import UserProfile, Role


class Command(BaseCommand):
    help = 'Seed demo users with hierarchy'

    def handle(self, *args, **options):
        PASSWORD = 'demo1234'

        # Super Admin
        sa_user, _ = User.objects.get_or_create(
            username='superadmin',
            defaults={'first_name': 'Super', 'last_name': 'Admin', 'is_staff': True, 'is_superuser': True},
        )
        sa_user.set_password(PASSWORD)
        sa_user.save()
        sa_profile, _ = UserProfile.objects.get_or_create(
            user=sa_user, defaults={'role': Role.SUPERADMIN},
        )

        # Manager 1
        m1_user, _ = User.objects.get_or_create(
            username='manager1',
            defaults={'first_name': 'Budi', 'last_name': 'Santoso'},
        )
        m1_user.set_password(PASSWORD)
        m1_user.save()
        m1_profile, _ = UserProfile.objects.get_or_create(
            user=m1_user, defaults={'role': Role.MANAGER},
        )

        # Manager 2
        m2_user, _ = User.objects.get_or_create(
            username='manager2',
            defaults={'first_name': 'Siti', 'last_name': 'Rahma'},
        )
        m2_user.set_password(PASSWORD)
        m2_user.save()
        m2_profile, _ = UserProfile.objects.get_or_create(
            user=m2_user, defaults={'role': Role.MANAGER},
        )

        # Supervisors under Manager 1
        for i, (first, last) in enumerate([
            ('Andi', 'Pratama'),
            ('Dewi', 'Lestari'),
            ('Fajar', 'Nugroho'),
        ], start=1):
            s_user, _ = User.objects.get_or_create(
                username=f'supervisor{i}',
                defaults={'first_name': first, 'last_name': last},
            )
            s_user.set_password(PASSWORD)
            s_user.save()
            UserProfile.objects.get_or_create(
                user=s_user,
                defaults={'role': Role.SUPERVISOR, 'manager': m1_profile},
            )

        # Supervisors under Manager 2
        for i, (first, last) in enumerate([
            ('Rina', 'Wijaya'),
            ('Hadi', 'Kurniawan'),
        ], start=4):
            s_user, _ = User.objects.get_or_create(
                username=f'supervisor{i}',
                defaults={'first_name': first, 'last_name': last},
            )
            s_user.set_password(PASSWORD)
            s_user.save()
            UserProfile.objects.get_or_create(
                user=s_user,
                defaults={'role': Role.SUPERVISOR, 'manager': m2_profile},
            )

        # Admin (Helpdesk)
        a_user, _ = User.objects.get_or_create(
            username='admin1',
            defaults={'first_name': 'Yuni', 'last_name': 'Astuti'},
        )
        a_user.set_password(PASSWORD)
        a_user.save()
        UserProfile.objects.get_or_create(
            user=a_user, defaults={'role': Role.ADMIN},
        )

        # Scoring
        sc_user, _ = User.objects.get_or_create(
            username='scoring1',
            defaults={'first_name': 'Prof.', 'last_name': 'Reviewer'},
        )
        sc_user.set_password(PASSWORD)
        sc_user.save()
        UserProfile.objects.get_or_create(
            user=sc_user, defaults={'role': Role.SCORING},
        )

        self.stdout.write(self.style.SUCCESS(
            '\nDemo data berhasil dibuat!\n\n'
            'Hierarchy:\n'
            '  Manager 1 (Budi Santoso) — manager1\n'
            '    ├── Supervisor 1 (Andi Pratama) — supervisor1\n'
            '    ├── Supervisor 2 (Dewi Lestari) — supervisor2\n'
            '    └── Supervisor 3 (Fajar Nugroho) — supervisor3\n'
            '  Manager 2 (Siti Rahma) — manager2\n'
            '    ├── Supervisor 4 (Rina Wijaya) — supervisor4\n'
            '    └── Supervisor 5 (Hadi Kurniawan) — supervisor5\n'
            '  Admin (Yuni Astuti) — admin1\n'
            '  Scoring (Prof. Reviewer) — scoring1\n'
            '  Super Admin — superadmin\n\n'
            'Password semua: demo1234'
        ))
