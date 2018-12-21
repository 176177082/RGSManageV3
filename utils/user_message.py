# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# TODO 这个是上个版本没有用的东东，删除掉
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        # 'user_id': user.id,
        # 'username': user.username
    }
