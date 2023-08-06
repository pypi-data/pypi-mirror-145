from http import HTTPStatus

import pytest
import responses
from django.contrib.auth import get_user_model
from django.urls import reverse

from terraso_allauth.views import TerrasoOAuth2Adapter

User = get_user_model()


def test_adapter_loads_url_from_settings(settings):
    url = "https://testing.terraso.org/"
    settings.TERRASO_BASE_API_URL = url

    assert TerrasoOAuth2Adapter(None).terraso_base_url == url


def test_adapter_apppend_slash_to_base_url(settings):
    url = "https://testing.terraso.org"
    settings.TERRASO_BASE_API_URL = url

    assert TerrasoOAuth2Adapter(None).terraso_base_url == url + "/"


def test_adapter_default_base_url():
    assert TerrasoOAuth2Adapter(None).terraso_base_url == "https://api.terraso.org/"


def test_adapter_builds_access_token_url():
    adapter = TerrasoOAuth2Adapter(None)

    assert f"{adapter.terraso_base_url}oauth/token/" in adapter.access_token_url


def test_adapter_builds_authorize_url():
    adapter = TerrasoOAuth2Adapter(None)

    assert f"{adapter.terraso_base_url}auth/authorize" == adapter.authorize_url


def test_adapter_builds_profile_url():
    adapter = TerrasoOAuth2Adapter(None)

    assert f"{adapter.terraso_base_url}oauth/userinfo" == adapter.profile_url


@pytest.mark.django_db
def test_login_view_is_redirect_on_post(client):
    response = client.post(reverse("terraso_login"))

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db
def test_full_signup_flow_with_success(client):
    user_email = "testing-user@example.org"
    user_first_name = "Tina"
    user_last_name = "Terrarina"

    # It's necessary call login POST to initialize related session data
    client.post(reverse("terraso_login"))
    _, state_verifier = client.session.get("socialaccount_state")

    with responses.RequestsMock() as resp:
        resp.add(
            method=responses.POST,
            url="https://api.terraso.org/oauth/token/",
            json={
                "access_token": "mocked-access",
                "refresh_token": "mocked-refresh",
                "expires_in": 12345,
            },
        )
        resp.add(
            method=responses.GET,
            url="https://api.terraso.org/oauth/userinfo",
            json={
                "sub": "1234567890",
                "email": user_email,
                "given_name": user_first_name,
                "family_name": user_last_name,
            },
        )

        response = client.get(
            reverse("terraso_callback"),
            {"code": "testing-code-123", "state": state_verifier},
        )

        assert response.status_code == HTTPStatus.FOUND

    user = User.objects.first()
    assert user.email == user_email
    assert user.first_name == user_first_name
    assert user.last_name == user_last_name
