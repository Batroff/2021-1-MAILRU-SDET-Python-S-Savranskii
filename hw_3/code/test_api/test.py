from test_api.base import ApiBase


class TestCampaign(ApiBase):

    def test_create_remove(self):
        campaign_name = self.api_dashboard.post_create_campaign()
        campaign = self.api_dashboard.get_campaign(campaign_name)
        assert campaign['exists'] is True

        self.api_dashboard.remove_campaign(campaign['id'])
        campaign = self.api_dashboard.get_campaign(campaign_name)
        assert campaign['exists'] is False


class TestSegment(ApiBase):

    def test_create(self):
        source_id = self.api_segment.create_vk_group_source()
        segment_id = self.api_segment.create_segment(source_id=source_id)
        assert self.api_segment.get_segment(segment_id=segment_id) is True
