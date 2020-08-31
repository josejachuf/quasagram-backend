# coding: utf8

from emmett import now, session
from emmett.orm import Model, Field, refers_to

def bool2str(value):
    if value:
        return 'Sí'
    return 'No'

def get_user():
    user_id = None
    try:
        if session.auth:
            user_id = session.auth.user.id
        elif session.user:
            user_id = session.user.id
        else:
            pass
    except:
        pass

    return user_id


def local_now():
    return now().in_timezone('America/Cordoba')


class Signature(Model):
    refers_to (
        {'created_by': 'User'},
        {'updated_by': 'User'}
        )

    created_at = Field.datetime()
    updated_at = Field.datetime()

    #~ validation = {
        #~ 'created_by': {'allow': 'empty'},
        #~ 'updated_by': {'allow': 'empty'},
    #~ }

    default_values = {
        'created_by': lambda: get_user(),
        'updated_by': lambda: get_user(),
        'created_at': lambda: local_now(),
        'updated_at': lambda: local_now(),
    }

    update_values = {
        'updated_by': lambda: get_user(),
        'updated_at': lambda: local_now(),

    }

    fields_rw = {
        'created_by': False,
        'updated_by': False,
        'created_at': False,
        'updated_at': False,
    }