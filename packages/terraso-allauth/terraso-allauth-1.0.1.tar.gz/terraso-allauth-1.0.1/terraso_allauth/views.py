import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from django.conf import settings

from .provider import TerrasoProvider


class TerrasoOAuth2Adapter(OAuth2Adapter):
    provider_id = TerrasoProvider.id

    @property
    def terraso_base_url(self):
        if hasattr(settings, "TERRASO_BASE_API_URL") and settings.TERRASO_BASE_API_URL:
            terraso_base_url = settings.TERRASO_BASE_API_URL
        else:
            terraso_base_url = "https://api.terraso.org/"

        return terraso_base_url if terraso_base_url[-1] == "/" else f"{terraso_base_url}/"

    @property
    def access_token_url(self):
        return f"{self.terraso_base_url}oauth/token/"

    @property
    def authorize_url(self):
        return f"{self.terraso_base_url}auth/authorize"

    @property
    def profile_url(self):
        return f"{self.terraso_base_url}oauth/userinfo"

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            params={"access_token": token.token},
        )
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(TerrasoOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(TerrasoOAuth2Adapter)
