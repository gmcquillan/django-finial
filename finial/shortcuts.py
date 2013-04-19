from finial.models import UserTemplateOverride

from django.conf import settings
from django.conf.urls.defaults import patterns, url

# This is dangerious, we should be wary of using this as overrides grow.
# Since this gets loaded before settings get modified by middleware,
# we need all of the static assets to be served.
# This code should *never* be run in production!!!!

def create_local_override_urls(root_urlpatterns):
    """Create URL paths for static assets for overrides in development mode."""
    if not settings.DEBUG:
        # Protect against people accidentally running this in production.
        return root_urlpatterns

    overrides = UserTemplateOverride.objects.all()
    for override in overrides:
        url_regex = r'^static/{0}/(?P<path>.*)$'.format(
            override.override_dir.replace('/', '')
        )
        dir_path = '{0}{1}{2}'.format(
            settings.PROJECT_PATH,  override.override_dir, '_staticfiles/'
        )
        root_urlpatterns += patterns('',
            url(url_regex, 'django.views.static.serve',{
                'document_root': dir_path,
            }),
        )

    return root_urlpatterns