import allure

from test_api.base import ApiBaseCase


class TestAppStatus(ApiBaseCase):

    @allure.description("Get app status, expect {'status': 'ok'}, headers: {'Content-Type': 'application/json'}")
    def test_status(self):
        resp = self.app_api_client.get_status()

        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json() == {"status": "ok"}
