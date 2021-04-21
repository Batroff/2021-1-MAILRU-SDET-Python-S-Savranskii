from selenium.webdriver.common.by import By


class BasePageLocators:
    OPEN_LOGIN_FORM = (By.XPATH, '//div[text()="Войти"]')

    # Login form
    FORM_EMAIL = (By.XPATH, '//input[contains(@class, "authForm") and @name="email"]')
    FORM_PASSWORD = (By.XPATH, '//input[contains(@class, "authForm") and @name="password"]')
    FORM_SUBMIT = (By.XPATH, '//div[contains(@class, "authForm") and text()="Войти"]')
    FORM_WRONG_DATA_FORMAT = (By.XPATH, '//div[text()="Введите email или телефон"]')


class DashboardPageLocators(BasePageLocators):
    CREATE_FIRST_CAMPAIGN = (By.XPATH, '//a[@href="/campaign/new"]')
    CREATE_CAMPAIGN = (By.XPATH, '//div[@data-test="button"]//div[text()="Создать кампанию"]')

    CAMPAIGN_CELL = (By.XPATH, '//div[@data-entity-type="campaign"]')
    CAMPAIGN_NAME_TEMPLATE = (By.XPATH, CAMPAIGN_CELL[1] + '//a[text()="{0}"]')
    CAMPAIGN_CHECKBOX = (By.XPATH, f'//div[@data-entity-type="campaign" and {CAMPAIGN_NAME_TEMPLATE[1]}]'
                                   f'//input[@type="checkbox"]')
    CAMPAIGN_ACTIONS = (By.XPATH, '//span[text()="Действия"]')
    CAMPAIGN_REMOVE = (By.XPATH, '//li[text()="Удалить"]')

    HEAD_MENU_LINK_TEMPLATE = (By.XPATH, '//div[contains(@class, "head")]//a[text()="{0}"]')


class LoginPageLocators(BasePageLocators):
    ERROR = (By.XPATH, '//div[text()="Error"]')


class CampaignPageLocators(BasePageLocators):
    OBJECTIVE_CONTAINER = (By.XPATH, '//div[@data-scroll-name="objective"]')
    OBJECTIVE_TEMPLATE = (By.XPATH, OBJECTIVE_CONTAINER[1] + '//div[text()="{0}"]')

    OBJECTIVE_LINK_INPUT = (By.XPATH, '//input[@placeholder="Введите ссылку"]')  # @data-gtm-id="ad_url_text"

    CAMPAIGN_NAME = (By.CSS_SELECTOR, 'div.campaign-name input[type="text"]')

    ADS_FORMAT_CONTAINER = (By.XPATH, '//div[@data-scroll-name="banner-formats"]')
    ADS_FORMAT_TEMPLATE = (By.XPATH, ADS_FORMAT_CONTAINER[1] + '//span[text()="{0}"]')
    ADS_FORMAT_INPUT = (By.XPATH, '//div[@data-pattern-name="image_240x400"]//input[@type="file"]')

    CREATE_BTN = (By.XPATH, '//button[@data-class-name="Submit"]//div[text()="Создать кампанию"]')


class SegmentPageLocators(BasePageLocators):
    GO_TO_GROUPS_VK_OK = (By.XPATH, '//span[text()="Группы ОК и VK"]')
    GROUP_LINK_INPUT = (By.XPATH, '//input[contains(@placeholder, "Введите ссылку на группу")]')
    GROUPS_SELECT_ALL = (By.XPATH, '//div[@data-test="select_all"]')
    GROUPS_ADD_SELECTED = (By.XPATH, '//div[text()="Добавить выбранные"]')
    GROUP_ROW_TEMPLATE = (By.XPATH, '//tr[.//span[text()="{0}"]]')
    GROUP_ROW_ID = (By.XPATH, '//td[@data-id="id"]')

    SEGMENT_LIST_BTN = (By.XPATH, '//span[text()="Список сегментов"]')

    CREATE_FIRST_SEGMENT = (By.XPATH, '//a[text()="Создайте"]')
    CREATE_SEGMENT = (By.XPATH, '//div[text()="Создать сегмент"]')

    SELECT_GROUPS_TARGETING = (By.XPATH, '//div[text()="Группы ОК и VK"]')
    GROUP_CHECKBOX = (By.XPATH, '//div[.//span[contains(text(), "{0}")]]/input[@type="checkbox"]')
    SEGMENT_ADD_BTN = (By.XPATH, '//div[text()="Добавить сегмент"]')
    SEGMENT_INPUT_NAME = (By.XPATH, '//div[@class="js-segment-name"]//input')

    SEGMENT_NAME_TEMPLATE = (By.XPATH, '//div[@role="rowgroup"]//a[contains(text(), "{0}")]')
    SEGMENT_CHECKBOX_TEMPLATE = (By.XPATH, '//div[contains(@data-test, "id-{0}")]//input[@type="checkbox"]')
    SEGMENT_ACTIONS = (By.XPATH, '//div[@data-test="select"]//span[text()="Действия"]')
    SEGMENT_ACTION_REMOVE = (By.XPATH, '//li[@data-id="remove"]')
    SEGMENT_REMOVE_SUCCESS = (By.XPATH, '//div[text()="1 сегмент был удален."]')

    SEGMENTS_SEARCH = (By.XPATH, '//div[contains(@class, "search")]//input')
    SEARCH_FOUND = (By.XPATH, '//ul[@data-test="undefined_list"]')
    SEARCH_NOT_FOUND = (By.XPATH, '//li[@data-test="nothing"]')
