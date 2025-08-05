from core.models import Pages


def get_support_service_obj():
    pages = Pages.objects.all().order_by('title')
    return pages
