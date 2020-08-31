# coding: utf8
import json
from pywebpush import webpush, WebPushException
from emmett.orm import Field, after_insert
from .subscriptions import Subscription
from .signature import Signature

VAPID_PUBLIC_KEY = 'XXX'
VAPID_PRIVATE_KEY = 'XXX'

VAPID_CLAIMS = {
    "sub": "mailto:jjachuf@gmail.com"
}


class Post(Signature):
    tablename = "posts"
    caption = Field.string(length=250)
    location = Field.string(length=250)
    photo = Field.upload()
    date = Field.datetime()

    default_values = {
    }

    validation = {
        'caption': {'presence': True},
        'location': {'presence': True}
    }

    @after_insert
    def send_notification(self, fields, rid):
        # user_id = recover from created post
        user_id = 5
        subscriptions = Subscription.by_user(user_id).select()

        message = {"title": "Post created",
                   "body": "Este es el cuerpo de la notificación",
                   "openUrl": "/#/"
                   }

        for subscription in subscriptions:
            try:
                webpush(
                    subscription_info=json.loads(json.dumps(subscription.subscription)),
                    data=json.dumps(message),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims=VAPID_CLAIMS
                )
            except WebPushException as ex:
                if '410 Gone' in str(ex):
                    subscription.delete_record()


