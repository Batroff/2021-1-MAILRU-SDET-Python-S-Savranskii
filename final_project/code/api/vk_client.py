import json

from api.client import ApiClient


class VkApiClient(ApiClient):

    def get_vk_id(self, username):
        return self._request(method='GET', location=f'vk_id/{username}', jsonify=True)["vk_id"]

    def add_vk_id(self, username, vk_id):
        data = {
            "username": username,
            "vk_id": vk_id
        }

        return self._request(method='POST', location=f'vk_id_add', data=json.dumps(data))
