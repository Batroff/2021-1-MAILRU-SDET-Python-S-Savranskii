import allure
import pytest

from base_tests.base import BaseCase


class TestWrongLogin(BaseCase):

    authorize = False

    @pytest.mark.UI
    @allure.description('Test: wrong data format')
    def test_format_negative(self):
        self.base_page.login(login='testing_data', password='some_pas')

        assert self.base_page.find_wrong_format_error() is True

    @pytest.mark.UI
    @allure.description('Test: wrong account data')
    def test_account_negative(self):
        self.base_page.login(login='wrong_email@mail.ru', password='password')
        login_page = self.go_to_login_page()

        assert login_page.find_error() is True


class TestCampaign(BaseCase):

    @pytest.mark.UI
    @allure.description('Test: create new campaign and check exist of it')
    def test_create(self, repo_root, time_now):
        campaign_page = self.dashboard_page.go_to_campaign_page()
        campaign_name = campaign_page.create_campaign(repo_root, time_now)

        assert self.dashboard_page.is_opened(self.dashboard_page._url_contains)
        assert self.dashboard_page.campaign_exists(campaign_name)

        self.dashboard_page.remove_campaign(campaign_name)
        self.dashboard_page.refresh_page()


class TestSegments(BaseCase):

    @pytest.mark.UI
    @allure.description('Test: create new segment and check existence of it')
    def test_create(self, time_now):
        segment_page = self.dashboard_page.go_to_segment_page()

        segment_name = segment_page.create_segment(time_now, name_prefix='test_create')
        assert segment_page.segment_exists(segment_name) == "Exists"

    @pytest.mark.UI
    @allure.description('Test: remove created segment')
    def test_remove(self, time_now):
        segment_page = self.dashboard_page.go_to_segment_page()

        segment_name = segment_page.create_segment(time_now, name_prefix='test_remove')

        segment_page.remove_segment(name=segment_name)
        segment_page.refresh_page()
        assert segment_page.segment_exists(name=segment_name) == "Not exists"
