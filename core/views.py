from datetime import date
from django.views import View
from django.contrib import messages
from core.models import SupportPreference, ContactMessage, Event, Appointment, Pages, FAQ
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from utils.call_models import get_support_service_obj


class IndexView(View):
    template_name = 'index.html'
    page_name = 'Welcome'

    def get(self, request):
        events = Event.objects.all()
        faq_list = FAQ.objects.all()[:6]
        return render(request, self.template_name, {
            "page_name": self.page_name,
            "events": events,
            "pages": get_support_service_obj(),
            "faqs": faq_list
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
            "success": True,
            "pages": get_support_service_obj()
        })


class DashboardView(LoginRequiredMixin, View):
    """Displays the user dashboard."""
    template_name = 'dashboard.html'
    page_name = 'Dashboard'
    pre_objs = SupportPreference.objects.all()

    def get(self, request):
        return render(request, self.template_name, {
            'page_name': self.page_name,
            'pre_objs': self.pre_objs,
            "pages": get_support_service_obj()

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
            "pages": get_support_service_obj()
        })


class BookAppointmentView(View):
    def post(self, request):
        Appointment.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            appointment_with=request.POST.get('appointment_with'),
            appointment_datetime=request.POST.get('appointment_datetime'),
        )
        return redirect('home')


class JoinUsView(View):
    template_name = 'join_us.html'
    page_name = 'Join Us'

    def get(self, request):
        return render(request, self.template_name, {
            "page_name": self.page_name,
            "pages": get_support_service_obj()
        })


class PagesView(View):
    template_name = 'pages.html'
    page_name = 'Support Service'

    def get(self, request, slug):
        page = Pages.objects.get(slug=slug)
        page_name = f'{self.page_name} | {page.title}'
        return render(request, self.template_name, {
            "page_name": page_name,
            "page": page,
            "pages": get_support_service_obj()
        })


class FaqView(View):
    template_name = 'faq.html'
    page_name = 'FAQ'

    def get(self, request):
        query = request.GET.get('q', '')
        faq_list = FAQ.objects.all()

        if query:
            faq_list = faq_list.filter(
                Q(question__icontains=query) | Q(answer__icontains=query)
            )

        paginator = Paginator(faq_list, 5)  # Show 5 FAQs per page
        page_number = request.GET.get('page')
        faqs = paginator.get_page(page_number)

        return render(request, self.template_name, {
            "page_name": self.page_name,
            "faqs": faqs,
            "pages": get_support_service_obj(),
            "query": query
        })
