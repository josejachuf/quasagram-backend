# coding: utf8

from emmett import request, response
from emmett.tools import ServicePipe

from backend import app
from backend.modules.cors import CORSPipe
# from backend.modules.apiauth import SessionInitializer, \
#         ApiKeyPipe, UserFetcherPipe


api = app.module(__name__, 'api', url_prefix='api')
api.pipeline = [
                ServicePipe('json'),
                CORSPipe()
                ]

v1 = api.module(__name__, 'v1', url_prefix='v1')
v1.pipeline = [
               # SessionInitializer(),
               # ApiKeyPipe(),
               # UserFetcherPipe()
               ]

@v1.route()
def test():
    return {'message': 'Test API V1'}