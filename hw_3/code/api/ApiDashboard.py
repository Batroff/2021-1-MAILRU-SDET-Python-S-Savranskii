import logging

import faker

from api.client import ApiClient

logger = logging.getLogger('test')


class ApiDashboard(ApiClient):

    def post_campaign_mass_action(self, campaign_id, status):
        headers = {
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/campaign/new',
            'X-CSRFToken': self.cookies['csrftoken'],
        }
        json = [
            {
                'id': campaign_id,
                'status': status
            }
        ]
        response = self._request('POST', location='api/v2/campaigns/mass_action.json', headers=headers, cookies=self.cookies,
                                 json=json, expected_status=[204])

    def remove_campaign(self, campaign_id):
        self.post_campaign_mass_action(campaign_id, 'deleted')

    def post_upload_banner(self):
        headers = {
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/campaign/new',
            'X-CSRFToken': self.cookies['csrftoken'],
        }

        filename = 'white.png'
        files = {
            'file': (filename, open(f'test_api/{filename}', 'rb'), 'image/png', {'data': {'width': 0, 'height': 0}}),
        }

        response = self._request('POST', 'api/v2/content/static.json', headers=headers, cookies=self.cookies,
                                 files=files, jsonify=True)
        logger.debug(f'static.json response body: {response}\n')

        return response['id']

    def get_campaign_objective_id(self):
        response = self._request('GET', location='api/v2/campaign_objective/traffic/urls.json',
                                 cookies=self.cookies, jsonify=True)
        logger.debug(f'campaign objective response = {response}')
        return response['items'][0].get('id')

    def get_campaign(self, campaign_name):
        headers = {
            'Connection': 'keep-alive',
            'Host': 'target.my.com',
            'Referer': 'https://target.my.com/dashboard',
        }
        params = {
            "_status__in": "active",
            "sorting": "-id",
            "limit": 10,
            "offset": 0
        }
        response = self._request('GET', location='api/v2/campaigns.json', headers=headers, params=params,
                                 cookies=self.cookies, jsonify=True)

        for item in response['items']:
            for name in item.values():
                if name == campaign_name:
                    return {'exists': True, 'id': item.get('id')}

        return {'exists': False, 'id': None}

    def post_create_campaign(self):
        banner_id = self.post_upload_banner()
        campaign_id = self.get_campaign_objective_id()

        name = f"campaign_{faker.Faker().bothify('####?????')}"
        data = {
            "name": name,
            "package_id": 961,
            "banners": [{
                "urls": {"primary": {"id": campaign_id}},
                "content": {"image_240x400": {"id": banner_id}},
                "name": ""
            }],
            "objective": "traffic",
        }
        headers = {
            'Host': 'target.my.com',
            'Content-Type': 'application/json',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/campaign/new',
            'X-CSRFToken': self.cookies['csrftoken'],
            'X-Campaign-Create-Action': 'new',
        }

        resp = self._request('POST', 'api/v2/campaigns.json', headers=headers, json=data, cookies=self.cookies)
        return name
