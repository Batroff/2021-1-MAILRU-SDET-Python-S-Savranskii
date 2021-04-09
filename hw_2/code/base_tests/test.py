import os
import allure
import pytest

from base_tests.base import BaseCase


class TestWrongLogin(BaseCase):

    authorize = False

    @pytest.mark.UI
    @allure.description('Test: wrong data format')
    def test_format_negative(self):
        self.base_page.login(login='testing_data', password='some_pas')

        wrong_data_error = self.base_page.find(self.base_page.locators.FORM_WRONG_DATA_FORMAT)
        wrong_data_error_text = self.base_page.wait_text_changed(wrong_data_error)
        assert 'Введите email или телефон' == wrong_data_error_text

    @pytest.mark.UI
    @allure.description('Test: wrong account data')
    def test_account_negative(self):
        self.base_page.login(login='wrong_email@mail.ru', password='password')
        login_page = self.get_login_page()

        assert login_page.find_error().text == 'Error'


class TestCampaign(BaseCase):

    @pytest.mark.UI
    @allure.description('Test: create new campaign and check exist of it')
    def test_create(self, repo_root, time_now):
        campaign_page = self.dashboard_page.create_campaign()
        campaign_page.choose_objective('Трафик')
        campaign_page.input_objective_link('mail.ru')

        campaign_name = f'test_campaign_{time_now}'
        campaign_page.input_campaign_name(campaign_name)

        campaign_page.choose_format('Баннер')
        file_path = os.path.join(repo_root, 'ui', 'banner.png')
        campaign_page.upload_banner(file_path)

        campaign_page.click(campaign_page.locators.CREATE_BTN)
        assert self.dashboard_page.is_opened(self.dashboard_page._url_contains)
        assert self.dashboard_page.campaign_exists(campaign_name)

        self.dashboard_page.select_campaign(campaign_name)
        self.dashboard_page.remove_campaign()
        self.dashboard_page.refresh_page()


class TestSegments(BaseCase):

    @pytest.mark.UI
    @allure.description('Test: create new segment and check existence of it')
    def test_create(self, time_now):
        segment_page = self.dashboard_page.go_to_segments()

        source_id = segment_page.create_group_source(link='https://vk.com/overhear_mtu')

        segment_name = f'test_create_{time_now}'
        segment_page.go_to_segment_list()
        segment_page.create_segment(name=segment_name, source_id=source_id)
        assert segment_page.segment_exists(name=segment_name) == "Exists"

    @pytest.mark.UI
    @allure.description('Test: remove created segment')
    def test_remove(self, time_now):
        segment_page = self.dashboard_page.go_to_segments()

        source_id = segment_page.create_group_source(link='https://vk.com/overhear_mtu')

        segment_name = f'test_remove_{time_now}'
        segment_page.go_to_segment_list()
        segment_page.create_segment(name=segment_name, source_id=source_id)

        segment_page.remove_segment(name=segment_name)
        segment_page.refresh_page()
        assert segment_page.segment_exists(name=segment_name) == "Not exists"
