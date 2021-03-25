from base import BaseCase
import pytest


class TestSite(BaseCase):
    mail = "testing.mail.py@mail.ru"
    pas = "uaProRYIi24"

    @pytest.mark.UI
    def test_login(self):
        self.login(self.mail, self.pas)
        assert "Кампании" in self.driver.title
        assert self.driver.current_url == "https://target.my.com/dashboard"

    @pytest.mark.UI
    def test_logout(self):
        self.login(self.mail, self.pas)
        self.logout()
        assert "Рекламная платформа myTarget" in self.driver.title
        assert self.driver.current_url == "https://target.my.com/"

    @pytest.mark.UI
    def test_contact_info(self):
        name = "UserName"
        phone = "88005553535"
        email = "test@mail.ru"

        self.login(self.mail, self.pas)

        self.switch_page("Профиль")
        self.contacts_change_name(name=name)
        self.contacts_change_phone(phone=phone)
        self.contacts_change_email(email=email)
        self.contacts_save_changes(timeout=3)

        self.driver.refresh()

        user_info = self.contacts_get_info(timeout=5)
        assert user_info["name"] == name
        assert user_info["phone"] == phone
        assert user_info["email"] == email

    @pytest.mark.parametrize(
        "page,expected_page_url",
        [
            ("Баланс", "https://target.my.com/billing#deposit"),
            ("Статистика", "https://target.my.com/statistics/summary"),
        ]
    )
    @pytest.mark.UI
    def test_page_switch(self, page, expected_page_url):
        self.login(self.mail, self.pas)
        self.switch_page(page)
        assert self.driver.current_url in expected_page_url
