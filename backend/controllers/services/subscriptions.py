# coding: utf8
from backend import Subscription
from . api import v1

subscriptions = v1.rest_module(__name__,
                       name='api_subscriptions',
                       model=Subscription,
                       url_prefix='subscriptions'
                       )