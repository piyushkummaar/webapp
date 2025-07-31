from django.urls import path
from .views import IndexView, DashboardView, SupportRedirectView


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('preference/', DashboardView.as_view(), name='dashboard'),
    path('support-redirect/', SupportRedirectView.as_view(), name='support_redirect'),
]