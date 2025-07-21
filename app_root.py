from os import wait

from quart_cors import cors
from models.build import Builder
from functools import wraps


from utils.xquart import Blueprint, request, abort
from config import config
# from utils.logger import logger

# Authorities

def root(f):
    """ Auth root user. """
    @wraps(f)
    async def decor(*args, **kwargs):
        if not config.root_auth.enable:
            return await f(*args, **kwargs)
        secret = request.headers.get('secret')
        if not secret or secret != config.project.secret:
            abort(401, 'Root authentication failed')
        return await f(*args, **kwargs)
    return decor


# Blueprint
app = Blueprint('root', __name__, url_prefix='/root/api')
app = cors(app)

@app.route('/getkey')
@root
async def get_key():
    return {"key": config.api_auth.authid}

@app.post('/build')
@root
async def build():
    ret = Builder.build_docs()
    if not ret:
        abort(500, 'failed')
        
    return {"status": "success"}


