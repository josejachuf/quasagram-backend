# coding: utf8
from emmett import Form
from emmett.orm import Field, has_many, rowattr
from emmett.tools.auth import AuthUser

class User(AuthUser):
    tablename = 'auth_users'

    avatar = Field.upload(autodelete=True)
    email = Field.string(length=255)

    has_many(
        {'suscripciones': 'Suscripcion.user'},
        {'posts': 'Post.user'},
    )

    default_vales =  {
    }

    validation = {
        'email': {'is': 'email'},
    }

    form_labels = {
        'email': 'Correo Electrónico',
        'password': 'Contraseña',
        'first_name': 'Nombre',
        'last_name': 'Apellido',
    }

    fields_rw = {
    }

    rest_rw = {
        # 'id': True,
    }

    @rowattr('nombre_completo')
    def _nombre_completo(self, row):
        return '%s %s'%(row.last_name.capitalize() or '', row.first_name.capitalize() or '')
