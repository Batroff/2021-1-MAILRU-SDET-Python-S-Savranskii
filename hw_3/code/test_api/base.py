import pytest


class ApiBase:

    authorize = True
    credentials = ('tes.tss@bk.ru', 'PURR2o2tti(t')
    redirect_urls = ('https://target.my.com/dashboard', 'https://account.my.com/login/')

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, api_dashboard, api_segment):
        self.api_client = api_client
        self.api_dashboard = api_dashboard
        self.api_segment = api_segment

        if self.authorize:
            api_client.post_login(*self.credentials, *self.redirect_urls)
