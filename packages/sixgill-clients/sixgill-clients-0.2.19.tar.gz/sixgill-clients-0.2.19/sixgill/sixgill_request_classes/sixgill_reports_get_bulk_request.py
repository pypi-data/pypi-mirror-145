from sixgill.sixgill_request_classes.sixgill_base_post_auth_request import SixgillBasePostAuthRequest


class SixgillReportsGetBulkRequest(SixgillBasePostAuthRequest):
    end_point = 'reports/reports'
    method = 'GET'

    def __init__(self, channel_id, access_token, limit=50, offset=0, sort_by=None,
                 sort_order=None, is_read=None, threats=None, id_list=None):
        super(SixgillReportsGetBulkRequest, self).__init__(channel_id, access_token)

        self.request.params['fetch_size'] = limit
        self.request.params['offset'] = offset
        self.request.params['sort_by'] = sort_by
        self.request.params['sort_order'] = sort_order
        self.request.params['is_read'] = is_read
        self.request.params['threat_level'] = threats
        self.request.params['id_list'] = id_list
