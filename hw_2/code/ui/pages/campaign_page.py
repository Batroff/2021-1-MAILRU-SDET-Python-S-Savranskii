import os

import allure

from ui.locators.pages_locators import CampaignPageLocators
from ui.pages.base_page import BasePage


class CampaignPage(BasePage):
    locators = CampaignPageLocators()
    url = 'https://target.my.com/campaign/new'

    def create_campaign(self, repo_root, time_now):
        self.choose_objective('Трафик')
        self.input_objective_link('mail.ru')

        campaign_name = f'test_campaign_{time_now}'
        self.input_campaign_name(campaign_name)

        self.choose_format('Баннер')
        file_path = os.path.join(repo_root, 'ui', 'banner.png')
        self.upload_banner(file_path)

        self.click(self.locators.CREATE_BTN)

        return campaign_name

    @allure.step('Choose objective')
    def choose_objective(self, name):
        self.click((self.locators.OBJECTIVE_TEMPLATE[0],
                    self.locators.OBJECTIVE_TEMPLATE[1].format(name)
                    ))

    @allure.step('Input objective link')
    def input_objective_link(self, link):
        self.keys_to_input(self.locators.OBJECTIVE_LINK_INPUT, link)

    @allure.step('Input campaign name')
    def input_campaign_name(self, name):
        self.keys_to_input(self.locators.CAMPAIGN_NAME, name)

    @allure.step('Choose campaign format')
    def choose_format(self, name):
        self.click(self.format_locator(self.locators.ADS_FORMAT_TEMPLATE, name))

    def upload_banner(self, filepath):
        self.upload_file(locator=self.locators.ADS_FORMAT_INPUT, file=filepath)
