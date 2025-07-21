from functools import wraps
from quart_cors import cors
from utils.xquart import Blueprint, request, abort
from models.markdown import Markdown, PrivateMarkdown
from config import config


# Authorities

def auth(f):
    """ Auth current Account (me) on HTTP protocol. """
    @wraps(f)
    async def decor(*args, **kwargs):
        if not config.api_auth.enable:
            return await f(*args, **kwargs)
        authid = request.cookies.get('authid') or request.headers.get('x-authid')
        if not authid or authid != config.api_auth.authid:
            abort(401, 'Authentication required')
        return await f(*args, **kwargs)
    return decor


# Blueprint
app = Blueprint('api', __name__, url_prefix='/api')
app = cors(app)

# Routes

@app.get('/v1/docs/<name>')
@auth
async def get_doc(name):
    private = request.args.get('private')
    if private and private == 'true':
        content = PrivateMarkdown.read_md(name)
    else:
        content = Markdown.read_md(name)
    
    return {
        'content': content
    }
    
@app.get('/v1/docs-list')
@auth
async def get_list_docs():
    includes = request.args.get('includes')
    
    content = {
        'public': Markdown.get_all_md_name()
    }

    if includes and 'private' in includes:
        private_content = PrivateMarkdown.get_all_md_name()
        if private_content:
            content['private'] = private_content
    
    return {
        'docs': content
    }

@app.post('/v1/docs')
@auth
async def save_doc():
    body = await request.get_json()
    private = body.get('private')
    md_content = body.get('content')
    md_name = body.get('name')
    
    if private:
        PrivateMarkdown.create_md(md_content, md_name)
    else :
        Markdown.create_md(md_content, md_name)

    return {
        'result': 'OK'
    }

@app.delete('/v1/docs/<name>')
@auth
async def delete_doc(name):
    private = request.args.get('private')
    if private and private == 'true':
        ret = PrivateMarkdown.delete_md(name)
    else:
        ret = Markdown.delete_md(name)
    
    if not ret:
        abort(404, 'N ot found')

    return {
        'result': 'ok'
    }
    