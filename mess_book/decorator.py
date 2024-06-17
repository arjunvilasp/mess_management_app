from django.shortcuts import redirect, reverse
from django.contrib.sessions.models import Session

def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'student_id' not in request.session and 'admin_id' not in request.session:
            return redirect(reverse('login'))  # Redirect to login if not logged in
        return view_func(request, *args, **kwargs)
    return wrapped_view
