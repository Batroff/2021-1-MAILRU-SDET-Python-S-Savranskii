import logging

import faker

from api.client import ApiClient

logger = logging.getLogger('test')


class ApiSegment(ApiClient):

    def create_segment(self, source_id):
        headers = {
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.cookies['csrftoken'],
        }
        name = f'segment_{faker.Faker().bothify("###??##")}'
        data = {
            'name': name,
            'pass_condition': 1,
            'relations': [{
                'object_type': "remarketing_vk_group",
                'params': {
                    'source_id': source_id,
                    'type': "positive"
                }
            }]
        }

        response = self._request('POST', 'api/v2/remarketing/segments.json', headers=headers, cookies=self.cookies,
                                 json=data, jsonify=True)
        return response['id']

    def get_segment(self, segment_id):
        headers = {
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/segments/segments_list',
            'X-CSRFToken': self.cookies['csrftoken'],
        }
        params = {
            'id': segment_id
        }
        response = self._request('GET', location='api/v2/coverage/segment.json', headers=headers, cookies=self.cookies,
                                 jsonify=True, params=params)

        for item in response['items']:
            for (key, value) in item.items():
                if key == 'id' and value == segment_id and item.get('status') is not "not found":
                    return True
        return False

    def create_vk_group_source(self):
        vk_id = self.get_vk_groups()
        self.post_vk_groups(vk_id)

        return vk_id

    def post_vk_groups(self, vk_id):
        headers = {
            'Host': 'target.my.com',
            'Origin': 'https://target.my.com',
            'Referer': 'https://target.my.com/segments/groups_list',
            'X-CSRFToken': self.cookies['csrftoken'],
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        data = {"object_id": vk_id}

        response = self.session.request('POST',
                                        url='https://target.my.com/api/v2/remarketing/vk_groups.json?fields=id,object_id,name,users_count,url',
                                        cookies=self.cookies,
                                        headers=headers, json=data)
        logger.debug(response.json())

    def get_vk_groups(self):
        response = self._request('GET', location='api/v2/vk_groups.json', params={'_q': "https://vk.com/overhear_mtu"},
                                 cookies=self.cookies, jsonify=True)
        logger.debug(f'vk_group response: {response}')
        return response['items'][0]['id']  # id
