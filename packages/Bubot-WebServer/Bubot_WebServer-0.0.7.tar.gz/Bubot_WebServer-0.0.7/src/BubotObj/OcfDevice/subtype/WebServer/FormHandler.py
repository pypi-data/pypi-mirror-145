from aiohttp import web
import json
import re
import os.path
from sys import path as syspath


class FormHandler(web.View):
    clear = re.compile('[^a-zA-Z0-9]')
    forms = dict()

    def __init__(self, request):
        web.View.__init__(self, request)
        if not self.forms:
            self.find_forms()

    async def get(self):
        device = self.request.match_info.get('device')
        obj_name = self.request.match_info.get('obj_name')
        form_name = self.request.match_info.get('form_name')
        try:
            file_name = self.forms[device][obj_name][f'{form_name}.form.json']
        except KeyError:
            try:
                file_name = self.forms['root'][obj_name][f'{form_name}.form.json']
            except KeyError as key:
                return web.HTTPInternalServerError(text=f"Form not found ({key})")

        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                # await asyncio.sleep(1)
                return web.json_response(data)
            except Exception as e:
                return web.Response(status=500, text=str(e))

    @classmethod
    def find_forms(cls, **kwargs):
        '''
        Ищем формы для каждого из предустановленных типов, в общем каталог и каталоге устройства
        :param kwargs:
        :return:
        '''

        def find_in_form_dir(_path, _device=None):
            obj_list = os.listdir(_path)
            for obj_name in obj_list:
                form_dir = os.path.normpath(f'{_path}/{obj_name}/forms')
                if not os.path.isdir(form_dir):
                    continue
                form_list = os.listdir(form_dir)
                for form_name in form_list:
                    if form_name[-5:] != ".json":
                        continue

                    if _device not in cls.forms:
                        cls.forms[_device] = {}
                    if obj_name not in cls.forms[_device]:
                        cls.forms[_device][obj_name] = {}
                    cls.forms[_device][obj_name][form_name] = os.path.normpath(f'{form_dir}/{form_name}')

        for path1 in syspath:
            bubot_dir = f'{path1}/BubotObj'
            if not os.path.isdir(bubot_dir):
                continue
            find_in_form_dir(bubot_dir, 'root')
            device_dir = f'{path1}/bubot/OcfDevice'
            if not os.path.isdir(device_dir):
                continue
            device_list = os.listdir(device_dir)
            for device in device_list:
                find_in_form_dir(os.path.normpath(f'{device_dir}/{device}'), device)
        pass
