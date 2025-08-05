from django.urls import path
from .views import (
    IndexView,
    DashboardView,
    SupportRedirectView,
    TermsConditionView,
    BookAppointmentView,
    JoinUsView,
    PagesView,
    FaqView
)


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('preference/', DashboardView.as_view(), name='dashboard'),
    path('support-redirect/', SupportRedirectView.as_view(), name='support_redirect'),
    path('terms-and-condition/', TermsConditionView.as_view(), name='terms_condition'),
    path('book-appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('join-us/', JoinUsView.as_view(), name='join_us'),
    path('faq/', FaqView.as_view(), name="faq"),
    path('support-service/<slug:slug>', PagesView.as_view(), name="pages"),

]