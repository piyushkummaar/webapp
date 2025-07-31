from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from accounts.models import CustomUser, PasswordResetToken


class RegisterView(View):
    """Handles user registration."""

    def get(self, request):
        return render(request, 'accounts/register.html', {'page_name': 'Register'})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                age=age
            )
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('dashboard')

        return render(request, 'accounts/register.html', {'page_name': 'Register'})


class LoginView(View):
    """Handles user login."""

    def get(self, request):
        return render(request, 'accounts/login.html', {'page_name': 'Login'})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or 'User'}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")

        return render(request, 'accounts/login.html', {'page_name': 'Login'})


class LogoutView(View):
    """Logs the user out and redirects to homepage."""

    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('accounts:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Displays the user profile."""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['page_name'] = 'Profile'
        return context


class ChangePasswordView(LoginRequiredMixin, View):
    """Allows the user to change their password."""

    def get(self, request):
        return render(request, 'accounts/change_password.html', {'page_name': 'Change Password'})

    def post(self, request):
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if not request.user.check_password(current):
            messages.error(request, "Current password is incorrect.")
        elif new != confirm:
            messages.error(request, "New passwords do not match.")
        elif len(new) < 8:
            messages.error(request, "New password must be at least 8 characters.")
        else:
            request.user.set_password(new)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password changed successfully.")
            return redirect('accounts:profile')

        return render(request, 'accounts/change_password.html', {'page_name': 'Change Password'})


class PasswordResetView(View):
    template_name = 'accounts/password_reset.html'
    page_name = 'Forget Password'

    def get(self, request):
        return render(request, self.template_name, {'page_name': self.page_name})

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No user with this email.")
            return render(request, self.template_name, {'page_name': self.page_name})

        # Create token
        token = PasswordResetToken.objects.create(user=user)
        reset_link = request.build_absolute_uri(
            reverse('accounts:password_reset_confirm', args=[token.random_string, str(token.token)])
        )
        # TODO: Email sent
        messages.success(request, f"Password reset link: {reset_link}")

        return render(request, self.template_name, {'page_name': self.page_name})


class PasswordResetConfirmView(View):
    template_name = 'accounts/password_reset_confirm.html'

    def get(self, request, token, random_str):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_expired():
                reset_token.delete()
                messages.error(request, "Reset link has expired.")
                return redirect('accounts:password_reset')
        except PasswordResetToken.DoesNotExist:
            messages.error(request, "Invalid or expired reset link.")
            return redirect('accounts:password_reset')

        return render(request, self.template_name)

    def post(self, request, token, random_str):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_expired():
                reset_token.delete()
                messages.error(request, "Reset link has expired.")
                return redirect('accounts:password_reset')
        except PasswordResetToken.DoesNotExist:
            messages.error(request, "Invalid reset link.")
            return redirect('accounts:password_reset')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, self.template_name, {'token': token})

        user = reset_token.user
        user.set_password(password)
        user.save()

        # Delete token after successful reset
        reset_token.delete()

        messages.success(request, "Password reset successfully. You can now log in.")
        return redirect('accounts:login')
