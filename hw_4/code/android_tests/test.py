import os
import re
import pytest

from android_tests.base import BaseCase


class TestChat(BaseCase):

    @pytest.mark.AndroidUI
    def test_russia_search(self):
        chat_page = self.main_page.go_to_chat_page()
        chat_page.find_in_chat('Russia')
        assert chat_page.get_card_title_russia() == 'Россия'

        chat_page.click_on_population_suggest()
        assert chat_page.get_card_title_population() == '146 млн.'

    @pytest.mark.AndroidUI
    def test_simple_calculation(self):
        chat_page = self.main_page.go_to_chat_page()
        chat_page.find_in_chat('2+2*2')
        assert chat_page.get_dialog_calc_result() == '6'


class TestFeedSource(BaseCase):

    @pytest.mark.AndroidUI
    def test_set_feed_source(self):
        settings_page = self.main_page.go_to_settings_page()
        source_page = settings_page.go_to_source_page()

        source_name = 'Вести FM'
        source_page.set_feed_source(source_name)
        assert source_page.is_feed_source_set(source_name)
        source_page.return_to_main_page()

        chat_page = self.main_page.go_to_chat_page()
        chat_page.find_in_chat('News')
        assert chat_page.get_player_vesti_fm() == 'Вести ФМ'


class TestSettings(BaseCase):

    @pytest.mark.AndroidUI
    def test_about_program(self, repo_root):
        settings_page = self.main_page.go_to_settings_page()

        about_page = settings_page.go_to_about_page()
        about_version, about_trademark = about_page.get_about_program()

        apk_file = self.driver.capabilities['app'].split(os.path.sep)[-1]
        apk_version = re.search(r'[\d+.]+\d+', apk_file).group(0)

        assert about_version == f'Версия {apk_version}'
        assert 'все права защищены' in about_trademark.lower()
