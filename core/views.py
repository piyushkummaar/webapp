from datetime import date
from django.views import View
from django.contrib import messages
from core.models import SupportPreference, ContactMessage, Event
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(View):
    template_name = 'index.html'
    page_name = 'Welcome'

    def get(self, request):
        events = Event.objects.all()
        return render(request, self.template_name, {
            "page_name": self.page_name,
            "events": events
            })

    def post(self, request):
        ContactMessage.objects.create(
            support_option=request.POST.get('support_option'),
            subject=request.POST.get('subject'),
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return render(request, self.template_name, {
            "page_name": self.page_name,
            "success": True
        })


class DashboardView(LoginRequiredMixin, View):
    """Displays the user dashboard."""
    template_name = 'dashboard.html'
    page_name = 'Dashboard'
    pre_objs = SupportPreference.objects.all()

    def get(self, request):

        return render(request, self.template_name, {
            'page_name': self.page_name,
            'pre_objs': self.pre_objs

        })


class SupportRedirectView(LoginRequiredMixin, View):
    """Redirects user based on selected support option and saves preference."""

    def post(self, request):
        selected_option = request.POST.get('support_option')

        if selected_option in ['medication', 'doctor', 'chat']:
            # Save or update preference

            if selected_option == 'medication':
                preference_val = 'Medication'
            elif selected_option == 'doctor':
                preference_val = 'Online Doctor Appointment'
            elif selected_option == 'chat':
                preference_val = 'Pharmacists Online Chat'
            else:
                preference_val = selected_option.capitalize()

            SupportPreference.objects.update_or_create(
                user=request.user,
                defaults={'preference': preference_val}
            )

            messages.success(request, "Your preference has been saved.")
        else:
            messages.error(request, "Invalid option selected")

        return redirect('accounts:profile')


class TermsConditionView(View):
    template_name = 'terms_and_condition.html'
    page_name = 'Terms & Conditions'

    def get(self, request):
        return render(request, self.template_name, {
            "page_name": self.page_name,
            "today_date": date.today().strftime('%B %d, %Y'),
        })

