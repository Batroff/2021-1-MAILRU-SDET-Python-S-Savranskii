import logging
import time

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from ui.locators.locators_android import BasePageLocators

CLICK_RETRY = 3
BASE_TIMEOUT = 5


logger = logging.getLogger('test')


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

        logger.info(f'{self.__class__.__name__} page is opening...')

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def press_back_key(self, count, timeout=0.2):
        for _ in range(count):
            self.driver.back()
            time.sleep(timeout)

    @staticmethod
    def format_locator(locator, *args) -> tuple:
        return locator[0], locator[1].format(*args)

    @allure.step('Clicking {locator}')
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i+1} of {CLICK_RETRY}...')
            try:
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

    def swipe_up(self, swipetime=200):
        """
        Базовый метод свайпа по вертикали
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, немного ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_to_element(self, swipe_method, locator, max_swipes, container_locator=None):
        """
        :param swipe_method: функция свайпа
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать вверх
        :param container_locator: локатор для свайпа
        """
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")

            if container_locator:
                swipe_method(locator=container_locator)
            else:
                swipe_method()
            time.sleep(2)
            already_swiped += 1

    def swipe_element_lo_left(self, locator):
        """
        :param locator: локатор, который мы ищем
        1. Находим наш элемент на экране
        2. Получаем его координаты (начала, конца по ширине и высоте)
        3. Находим центр элемента (по высоте)
        4. Делаем свайп влево, двигая центр элемента за его правую часть в левую сторону.
        """
        element = self.find(locator, 10)
        left_x = element.location['x']
        right_x = left_x + element.rect['width']

        window_width = self.driver.get_window_size()['width']
        logger.info(f'window_w: {window_width}, right_x: {right_x}')
        if right_x >= window_width:
            window_width = self.driver.get_window_size()['width']
            right_elem_x = left_x + element.rect['width']
            right_x = right_elem_x if right_elem_x < window_width else window_width
            right_x = (left_x + right_x) / 2  # right_x = middle_x

        upper_y = element.location['y']
        lower_y = upper_y + element.rect['height']
        middle_y = (upper_y + lower_y) / 2
        action = TouchAction(self.driver)
        action. \
            press(x=right_x, y=middle_y). \
            wait(ms=300). \
            move_to(x=left_x, y=middle_y). \
            release(). \
            perform()
