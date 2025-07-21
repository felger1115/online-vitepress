from types import SimpleNamespace
import config.env as env

project = SimpleNamespace(
    id='online-vitepress',
    secret=env.get('project.secret', '123www333'),
)

api_auth = SimpleNamespace(
    enable=env.get('api_auth.enable', True),
    authid=env.get('api_auth.authid', 'dddadmin'),
)

root_auth = SimpleNamespace(
    enable=env.get('root_auth.enable', True)
)
