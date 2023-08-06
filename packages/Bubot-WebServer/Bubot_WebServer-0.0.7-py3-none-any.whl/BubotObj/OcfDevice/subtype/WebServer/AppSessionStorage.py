import uuid
from time import time

from aiohttp_session import AbstractStorage, Session
from bson import json_util as json


class AppSessionStorage(AbstractStorage):
    def __init__(self, app, *, cookie_name="AIOHTTP_SESSION",
                 domain=None, max_age=None, path='/',
                 key_factory=lambda: uuid.uuid4().hex,
                 secure=None, httponly=True,
                 encoder=json.dumps, decoder=json.loads):
        super().__init__(cookie_name=cookie_name, domain=domain,
                         max_age=max_age, path=path, secure=secure,
                         httponly=httponly,
                         encoder=encoder, decoder=decoder)
        try:
            with open('sessions.json', 'r', encoding='utf-8') as file:
                app['sessions'] = json.loads(file.read())
        except Exception as err:
            pass
        self._key_factory = key_factory
        self.app = app

    async def load_session(self, request):
        def empty_session():
            return Session(None, data=None, new=True, max_age=self.max_age)

        cookie = self.load_cookie(request)
        if cookie is None:
            return empty_session()
        # key = self._decoder(cookie)
        key = cookie
        if key is None:
            return empty_session()
        try:
            stored_key = key
        except KeyError:
            return empty_session()
        data = self.app['sessions'].get(stored_key)
        if data is None:
            return empty_session()
        return Session(key, data=data, new=False, max_age=self.max_age)

    async def save_session(self, request, response, session):
        key = session.identity
        if key and not session.new and session.empty:  # закрыли сессию
            self.save_cookie(response, None, max_age=session.max_age)
            self.app['sessions'].pop(key)
            self.save_sessions()
            return

        if key is None:  # гостевая сессия
            key = self._key_factory()
            self.save_cookie(response, key,
                             max_age=session.max_age)
        else:
            if session.new:
                self.save_cookie(response, key, max_age=session.max_age)

        data = self._get_session_data(session)
        max_age = session.max_age
        if max_age is None:
            expire = 0
        elif max_age > 30 * 24 * 60 * 60:
            expire = int(time()) + max_age
        else:
            expire = max_age
        try:
            # stored_key = key['_id']
            stored_key = key
        except Exception:
            raise Exception('Bad session key_factory')

        data['expire'] = expire
        self.app['sessions'][stored_key] = data
        self.save_sessions()

    async def close(self):
        a = 1
        pass

    def save_sessions(self):
        with open('sessions.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.app['sessions'], ensure_ascii=False, indent=2))
