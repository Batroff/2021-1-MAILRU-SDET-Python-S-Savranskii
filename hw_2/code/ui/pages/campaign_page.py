import allure

from ui.locators.pages_locators import CampaignPageLocators
from ui.pages.base_page import BasePage


class CampaignPage(BasePage):
    locators = CampaignPageLocators()
    url = 'https://target.my.com/campaign/new'

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
        # self.click((self.locators.ADS_FORMAT_TEMPLATE[0],
        #             self.locators.ADS_FORMAT_TEMPLATE[1].format(name)
        #             ))

    def upload_banner(self, filepath):
        self.upload_file(locator=self.locators.ADS_FORMAT_INPUT, file=filepath)
