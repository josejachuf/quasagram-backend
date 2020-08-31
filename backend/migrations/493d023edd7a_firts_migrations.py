"""firts migrations

Migration ID: 493d023edd7a
Revises: 
Creation Date: 2020-08-25 16:36:52.651631

"""

from emmett.orm import migrations


class Migration(migrations.Migration):
    revision = '493d023edd7a'
    revises = None

    def up(self):
        self.create_table(
            'auth_users',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('email', 'string', length=255),
            migrations.Column('password', 'password', length=512),
            migrations.Column('registration_key', 'string', default='', length=512),
            migrations.Column('reset_password_key', 'string', default='', length=512),
            migrations.Column('registration_id', 'string', default='', length=512),
            migrations.Column('first_name', 'string', notnull=True, length=128),
            migrations.Column('last_name', 'string', notnull=True, length=128),
            migrations.Column('avatar', 'upload', length=512))
        self.create_table(
            'auth_groups',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('role', 'string', default='', length=255),
            migrations.Column('description', 'text'))
        self.create_table(
            'auth_memberships',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('user', 'reference auth_users', ondelete='CASCADE'),
            migrations.Column('auth_group', 'reference auth_groups', ondelete='CASCADE'))
        self.create_table(
            'auth_permissions',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('name', 'string', default='default', notnull=True, length=512),
            migrations.Column('table_name', 'string', length=512),
            migrations.Column('record_id', 'integer', default=0),
            migrations.Column('auth_group', 'reference auth_groups', ondelete='CASCADE'))
        self.create_table(
            'auth_events',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('client_ip', 'string', length=512),
            migrations.Column('origin', 'string', default='auth', notnull=True, length=512),
            migrations.Column('description', 'text', default='', notnull=True),
            migrations.Column('user', 'reference auth_users', ondelete='CASCADE'))
        self.create_table(
            'posts',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('caption', 'string', length=250),
            migrations.Column('location', 'string', length=250),
            migrations.Column('photo', 'upload', length=512),
            migrations.Column('date', 'datetime'),
            migrations.Column('created_by', 'reference auth_users', ondelete='SET NULL'),
            migrations.Column('updated_by', 'reference auth_users', ondelete='SET NULL'))
        self.create_table(
            'subscriptions',
            migrations.Column('id', 'id'),
            migrations.Column('created_at', 'datetime'),
            migrations.Column('updated_at', 'datetime'),
            migrations.Column('subscription', 'json'),
            migrations.Column('user_id', 'integer'),
            migrations.Column('created_by', 'reference auth_users', ondelete='SET NULL'),
            migrations.Column('updated_by', 'reference auth_users', ondelete='SET NULL'))

    def down(self):
        self.drop_table('subscriptions')
        self.drop_table('posts')
        self.drop_table('auth_events')
        self.drop_table('auth_permissions')
        self.drop_table('auth_memberships')
        self.drop_table('auth_groups')
        self.drop_table('auth_users')
