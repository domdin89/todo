from django.http import HttpResponseForbidden
from functools import wraps

def check_staff(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is a staff member
        if not request.user.is_staff:
            return HttpResponseForbidden("Accesso riservato al personale autorizzato")

        # Proceed with the original view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view
