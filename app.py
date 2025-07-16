from quart import redirect
from utils.xquart import XQuart
from app_api import app as api
from app_root import app as root

# Application server with blueprints

app = XQuart(__name__, static_folder='static', static_url_path='/static')
app.register_blueprint(api)
app.register_blueprint(root)

@app.route('/')
async def root():
    return redirect('/static/index.html', code=301)

# @app.before_serving
# async def startup():
#     pass

# @app.after_serving
# async def shutdown():
#     pass


# Development only
# ==========
# usage:
# $ ENV=dev QUART_DEBUG=1 QUART_APP=app:app quart run -h 0.0.0.0 -p 80
if __name__ == '__main__':
    from config import config
    from utils.logger import logger
    logger.warning('**********')
    logger.warning('* DO NOT run this script directly since it blocks hot-reload, see https://github.com/pallets/quart/issues/350 for further information.')
    logger.warning('* Try to run: ENV=dev QUART_DEBUG=1 QUART_APP=app:app quart run -h 0.0.0.0 -p 80')
    logger.warning('**********')

    host = '0.0.0.0'
    port = 80
    logger.info(str.format('Server listen at {}:{}', host, port))
    app.run(host=host, port=port, debug=config.env.debug)
