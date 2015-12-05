from blog import settings


def site_info(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_title': settings.SITE_TITLE,
        'site_description': settings.SITE_DESCRIPTION,
        'site_url': settings.SITE_URL,
    }