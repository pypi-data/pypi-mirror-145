from django.urls import reverse


def test_terraso_provider_url_is_found_by_allauth():
    url = reverse("terraso_login")
    assert url
