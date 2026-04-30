from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

# URL yang boleh diakses superuser di luar /admin/
_SUPERUSER_ALLOWED = ('/admin/', '/login/', '/logout/')


class SingleSessionMiddleware:
    """Paksa satu sesi per user. Jika login di perangkat lain, sesi lama otomatis logout."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Superuser hanya boleh di /admin/ — redirect ke sana jika akses halaman lain
            if request.user.is_superuser:
                if not request.path.startswith(_SUPERUSER_ALLOWED):
                    return redirect('/admin/')

            # Cek single session untuk user biasa
            try:
                profile = request.user.profile
                stored_key = profile.session_key
                current_key = request.session.session_key
                if stored_key and current_key and stored_key != current_key:
                    logout(request)
                    messages.warning(
                        request,
                        'Sesi Anda telah berakhir karena akun ini login di perangkat lain.',
                    )
                    return redirect('login')
            except Exception:
                pass
        return self.get_response(request)
