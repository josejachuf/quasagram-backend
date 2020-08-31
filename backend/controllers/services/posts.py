# coding: utf8
import datetime
from emmett import response, request, url
from emmett_rest import Serializer
from backend import Post
from . api import v1

def _url_photo(photo):
    host = request.host
    scheme = 'https'
    if '127.0.0.1' in host or 'localhost' in host:
         scheme = request.scheme

    return url('main.download', args=[photo], scheme=scheme, host=host)

class PostSerializer(Serializer):
    def imageUrl(self, row):
        return _url_photo(row.photo)

posts = v1.rest_module(__name__,
                       name='api_posts',
                       model=Post,
                       serializer=PostSerializer,
                       url_prefix='posts'
                       )
posts.allowed_sorts = ['date']


@posts.create()
async def add_post():
    response.status = 201
    attrs = await request.body_params
    files = await request.files
    f_photo = files.photo
    photo = Post.photo.store(f_photo.stream,f_photo.filename)

    r = Post.create(caption=attrs.caption,
                    location=attrs.location,
                    date=datetime.datetime.fromtimestamp(
                            int(attrs.date) / 1e3),
                    photo=photo
                    )
    if r.errors:
        response.status = 422
        return posts.error_422(r.errors)
    return posts.serialize_one(r.id)