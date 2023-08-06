from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import TerrasoProvider

urlpatterns = default_urlpatterns(TerrasoProvider)
