"""Tests for `django_urlconfchecks` package."""
import os

from django.core import checks
from django.test.utils import override_settings
from django.urls import URLPattern
from django.urls.resolvers import RoutePattern, get_resolver

from django_urlconfchecks.check import check_url_signatures, get_all_routes
from tests.dummy_project.views import year_archive
from tests.utils import error_eql

os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'


def test_correct_urls():
    """Test that no errors are raised when the urlconf is correct.

    Returns:
         None
    """
    with override_settings(ROOT_URLCONF='tests.dummy_project.urls.correct_urls'):
        errors = check_url_signatures(None)
        assert not errors


def test_incorrect_urls():
    """Test that errors are raised when the urlconf is incorrect.

    Returns:
        None
    """
    with override_settings(ROOT_URLCONF='tests.dummy_project.urls.incorrect_urls'):
        errors = check_url_signatures(None)
        expected_error = checks.Error(
            'For parameter `year`, annotated type int does not match expected `str` from urlconf',
            hint=None,
            obj=URLPattern(
                pattern=RoutePattern(route='articles/<str:year>/', is_endpoint=True),
                callback=year_archive,
                default_args={},
            ),
            id='urlchecker.E002',
        )
        assert len(errors) == 1

        assert error_eql(errors[0], expected_error)


def test_all_urls_checked():
    """Test that all urls are checked.

    Returns:
        None
    """
    with override_settings(ROOT_URLCONF='tests.dummy_project.urls.correct_urls'):
        resolver = get_resolver()
        routes = get_all_routes(resolver)
        assert len(list(routes)) == 3


def test_child_urls_checked():
    """Test that child urls are checked.

    Returns:
        None
    """
    with override_settings(ROOT_URLCONF='tests.dummy_project.urls.parent_urls'):
        resolver = get_resolver()
        routes = get_all_routes(resolver)
        assert len(list(routes)) == 3


def test_admin_urls_ignored():
    """Test that admin urls are ignored.

    Returns:
        None
    """
    with override_settings(ROOT_URLCONF='tests.dummy_project.urls.admin_urls'):
        resolver = get_resolver()
        routes = get_all_routes(resolver)
        assert len(list(routes)) == 0
