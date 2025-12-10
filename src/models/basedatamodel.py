from helper.config import get_settings


class BaseDataModel():
    def __init__(self, db_client:object):
        self.db_client = db_client
        self.setting = get_settings()

        




