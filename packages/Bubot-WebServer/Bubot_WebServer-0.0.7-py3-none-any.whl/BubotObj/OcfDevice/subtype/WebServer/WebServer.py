# from bubot.Client.OcfDevice.OcfDevice import OcfDevice
import asyncio
import json
import os.path

from aiohttp import web
from aiohttp_session import get_session, setup
from bson import ObjectId

# from bubot.Catalog.Client.WebServer import API
from Bubot.Core.DataBase.Mongo import Mongo as Storage
# from bubot.Core.DataBase.SqlLite import SqlLite as Storage
from Bubot.Core.FastStorage.Simple import SimpleFastStorage as FastStorage
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ResourceNotAvailable
from Bubot.Helpers.Helper import Helper
from Bubot.Ocf.Helper import find_drivers
from BubotObj.OcfDevice.subtype.Device import Device
from BubotObj.OcfDevice.subtype.Device.QueueMixin import QueueMixin
from BubotObj.OcfDevice.subtype.VirtualServer.VirtualServer import VirtualServer
from BubotObj.OcfDevice.subtype.WebServer.AppSessionStorage import AppSessionStorage
from BubotObj.OcfDevice.subtype.WebServer.FormHandler import FormHandler
# import logging
from BubotObj.OcfDevice.subtype.WebServer.HttpHandler import HttpHandler
from BubotObj.OcfDevice.subtype.WebServer.WsHandler import WsHandler
from .__init__ import __version__ as device_version


# _logger = logging.getLogger(__name__)


class WebServer(VirtualServer, QueueMixin):
    version = device_version
    file = __file__
    template = False
    forms = dict()

    def __init__(self, **kwargs):
        # self.drivers = []
        # self.resources = []
        # self.cache_schemas = {}
        self.schemas_dir = []
        self.net_devices = {}
        self.request_queue = asyncio.Queue()
        self.serial_queue_worker = None
        self.ws = {}
        self.runner = None
        VirtualServer.__init__(self, **kwargs)

    async def on_pending(self):
        # self.serial_queue_worker = asyncio.ensure_future(self.queue_worker(self.request_queue, 'request_queue'))
        await self.run_web_server()
        await super().on_pending()

    @async_action
    async def run_web_server(self, *, _action):

        # self = cls.init_from_file(**kwargs)
        # self.save_config()
        # self.log.info(f'{self.__class__.__name__} start up')
        app = web.Application(
            middlewares=[
                # session_middleware(SimpleCookieStorage()),
                # self.middleware_auth(),
                self.middleware_index
            ])
        app['device'] = self
        app['sessions'] = {}
        app['fast_storage'] = FastStorage()
        app['storage'] = Storage.connect(self)
        setup(app, self.get_session_storage(app, 'AppSessionStorage'))
        drivers = find_drivers(log=self.log)
        self.set_param('/oic/mnt', 'drivers', drivers)
        self.build_i18n(drivers)
        self.add_routes(app)
        port = self.get_param('/oic/con', 'port', 80)
        # app.on_startup.append(self.start_background_tasks)
        # app.on_cleanup.append(self.cleanup_background_tasks)
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, None, port)
        await site.start()
        self.log.info(f'{self.__class__.__name__} started up http://localhost:{port}')
        return app
        # web.run_app(app, port=port)

    @staticmethod
    async def start_background_tasks(app):
        pass
        # self = app['device']
        # app['device_task'] = asyncio.create_task(VirtualServer.main(self))

    @staticmethod
    async def cleanup_background_tasks(app):
        # if not app['main'].done():
        #     app['main'].cancel()
        #     await app['main']
        # if not app['broker'].done():
        #     app['broker'].cancel()
        #     await app['broker']
        pass

    def build_i18n(self, drivers):
        locales = {
            'en': {},
            'ru': {},
            'cn': {}
        }
        self.log.info('begin')
        for elem in drivers:
            _path = os.path.normpath(f'{drivers[elem]["path"]}/i18n')
            if not os.path.isdir(_path):
                continue
            for locale in locales:
                locale_path = os.path.normpath(f'{drivers[elem]["path"]}/i18n/{locale}.json')
                if not os.path.isfile(locale_path):
                    continue
                with open(locale_path, "r", encoding='utf-8') as file:
                    try:
                        _data = json.load(file)
                        Helper.update_dict(locales[locale], _data)
                    except Exception as err:
                        self.log.error(f'Build locale {locale} for driver {elem}: {str(err)}')

        i18n_dir = os.path.normpath(f'{self.path}/i18n')
        try:
            os.mkdir(i18n_dir)
        except FileExistsError:
            pass
        except Exception as err:
            raise ResourceNotAvailable(detail=f'{err} - {i18n_dir}', parent=err)
        for locale in locales:
            build_path = os.path.normpath(f'{i18n_dir}/{locale}.json')
            with open(build_path, "w", encoding='utf-8') as file:
                try:
                    json.dump(locales[locale], file, ensure_ascii=False)
                except Exception as err:
                    self.log.error(f'Build locale {locale}: {str(err)}')

        self.log.info('complete')

    def add_routes(self, app):
        self.log.info('add routes')
        for elem in self.get_param('/oic/mnt', 'drivers'):
            try:
                ui_view: Device = self.get_device_class(elem)()
                ui_view.add_route(app)  # todo сделать разводящую из всех доступных
            except NotImplementedError:
                pass
            except Exception as e:
                self.log.error('Error import_ui_handlers({1}): {0}'.format(e, elem))
        # for elem in app.router.routes():
        #     print(elem)
        pass

    def add_route(self, app):
        app.router.add_route('get', '/ws', WsHandler)
        app.router.add_route('*', '/api/{device}/{action}', HttpHandler)
        app.router.add_route('*', '/api/{device}/{obj_name}/{action}', HttpHandler)
        app.router.add_route('get', '/form/{device}/{obj_name}/{form_name}', FormHandler)
        # app.router.add_route('*', '/schema/{action}', SchemaHandler)
        app.router.add_static('/i18n', f'{self.path}/i18n')
        pass

    @staticmethod
    def middleware_auth():
        async def middleware_factory(app, handler):
            async def auth_handler(request):
                session = await get_session(request)
                if session.get("user"):
                    return await handler(request)
                else:
                    # auth = 0
                    try:
                        pass
                        # if issubclass(handler, Ui) and handler.need_auth(request):
                        #     raise web.HTTPFound(
                        #         "{0}?redirect={1}".format(app['bubot'].get_param('login_url'), request.path))
                        # auth = request.app['src_vue'][re.findall('^/src_vue/(.*)/', request.path)[0]]['param']['auth']
                    finally:
                        pass
                        # if auth:
                        # url = request.app.router['login'].url()

                return await handler(request)

            return auth_handler

        return middleware_factory

    @staticmethod
    @web.middleware
    async def middleware_index(request, handler, index='index.html'):
        # """Handler to serve index files (index.html) for static directories.
        #
        # :type request: aiohttp.web.Request
        # :returns: The result of the next handler in the chain.
        # :rtype: aiohttp.web.Response
        # """

        try:

            filename = request.match_info['filename']
            if not filename or filename.endswith('/'):
                filename = index
            request.match_info['filename'] = filename
        except KeyError:
            pass
        return await handler(request)

    # def get_schema_by_rt(self, rt):
    #     json_schema = JsonSchema4(cache=self.cache_schemas, dir=self.schemas_dir)
    #     return json_schema.load_from_rt(rt)

    async def on_notify_response(self, message, answer):
        try:
            self.log.debug('{0} receive notify {1} {2}'.format(
                self.__class__.__name__, message.to.di, message.to.href))
            for elem in self.ws:
                data = message.to_dict()
                await self.ws[elem].ws.send_json(data)
        except Exception as err:
            self.log.error('on_notify_response: {}'.format(err))

    @staticmethod
    def get_session_storage(app, name):
        # def cookie_encoder(data):
        #     return quote(json.dumps(data))
        #
        # def cookie_decoder(data):
        #     try:
        #         return json.loads(unquote(data))
        #     except:
        #         return None

        def get_app_session_storage():
            return AppSessionStorage(
                app,
                httponly=False,
                key_factory=lambda: str(ObjectId()),
                cookie_name="session",
                # encoder=cookie_encoder, decoder=cookie_decoder
            )

        available = {
            'AppSessionStorage': get_app_session_storage
        }
        return available[name]()
