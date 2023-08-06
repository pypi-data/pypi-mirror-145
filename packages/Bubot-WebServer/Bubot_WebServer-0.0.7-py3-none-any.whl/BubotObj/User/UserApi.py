from Bubot.Core.CatalogObjApi import CatalogObjApi
# from bubot.Helpers.Сryptography.SignedData import SignedData
from BubotObj.User.User import User


class UserApi(CatalogObjApi):
    name = "User"
    handler = User

