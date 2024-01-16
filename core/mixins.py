from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

class LoginRequiredMixin:
    login_url = redirect('accounts:login') 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
