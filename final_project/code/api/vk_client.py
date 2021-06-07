from api.client import ApiClient


class VkApiClient(ApiClient):

    def get_vk_id(self, username):
        return self._request(method='GET', location=f'vk_id/{username}', jsonify=True)["vk_id"]
