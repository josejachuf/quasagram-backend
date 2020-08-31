# coding: utf8
from emmett.orm import Field, scope
from .signature import Signature

class Subscription(Signature):
    tablename = "subscriptions"
    subscription = Field.json()
    user_id = Field.int()

    defaulf_values = {
        'user_id': 0
    }

    @scope('by_user')
    def _by_user(self, user_id):
        return self.user_id == user_id