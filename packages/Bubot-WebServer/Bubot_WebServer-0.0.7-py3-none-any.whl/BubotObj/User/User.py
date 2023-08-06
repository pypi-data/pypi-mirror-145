from Bubot.Core.Obj import Obj
from Bubot.Helpers.ActionDecorator import async_action
from Bubot.Helpers.ExtException import ExtException, AccessDenied, KeyNotFound
from Bubot.Helpers.Helper import ArrayHelper


class User(Obj):
    name = 'User'
    file = __file__

    @classmethod
    async def find_by_cert(cls, storage, cert, create=False):
        data = cert.get_user_data_from_cert()
        self = cls(storage)
        try:
            data = await self.find_by_keys(data['keys'])
            self.init_by_data(data)
        except KeyError:
            if create:
                self.init_by_data(data)
                await self.update()
            else:
                raise KeyError
        return self

    @property
    def db(self):
        return 'AuthService'

    @async_action
    async def add_auth(self, data, **kwargs):
        action = kwargs['_action']
        session = kwargs.get('session', {})
        user_id = session.get('user')
        if user_id:
            try:
                action.add_stat(await self.find_by_id(user_id, projection={'_id': 1, 'auth': 1}))
                res = action.add_stat(await self.push('auth', data))
            except KeyError:
                session['user'] = None
        res = action.add_stat(await self.query(
            filter={'auth.type': data['type'], 'auth.id': data['id']},
            projection={'_id': 1, 'auth': 1},
            limit=1
        ))
        if res:
            raise ExtException(message='Такой пользователь уже зарегистрирован')

        self.data = {
            'title': data['id'],
            'auth': [data]
        }
        res = action.add_stat(await self.update())
        return {}
        pass

    @async_action
    async def find_user_by_auth(self, _type, _id, **kwargs):
        action = kwargs["_action"]
        res = action.add_stat(await self.query(
            filter={
                'auth.type': _type,
                'auth.id': _id,
            },
            limit=1
        ))
        bad_password = Unauthorized()
        if not res:
            raise bad_password
        i = ArrayHelper.find(res[0]['auth'], _type, 'type')
        if i < 0:
            raise bad_password
        self.init_by_data(res[0])
        return res[0]['auth'][i]

    def get_default_account(self):
        accounts = self.data.get('account', [])
        if not accounts:
            return 'Bubot'

        _account = self.data.get('last_account')
        if _account is None:
            _account = accounts[0]
        return _account

    @classmethod
    @async_action
    async def check_right(cls, **kwargs):
        action = kwargs['_action']
        try:
            storage = kwargs['storage']
            user_ref = kwargs['user']
            account_id = kwargs['account']
            object_name = kwargs['object']
            level = kwargs['level']
            params = kwargs.get('params', {})
        except KeyError as key:
            raise KeyNotFound(detail=str(key))
        try:
            user = cls(storage, account_id=account_id, form='AccessRight')
            action.add_stat(await user.find_by_id(user_ref['_ref'].id))
            rights = user.data.get('right')
        except Exception as err:
            raise AccessDenied(parent=err)
        if not rights:
            raise AccessDenied(detail='Empty access list')
        try:
            _level = rights[object_name]['level']
        except Exception:
            raise AccessDenied(detail=object_name)
        if _level < level:
            raise AccessDenied(detail=object_name)
        pass
