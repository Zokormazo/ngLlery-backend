#coding=utf8

class Config:
    SITE_NAME = 'Argazkiak'
    SITE_DESCRIPTION = 'Gure familitxoko argazki bilduma'

    USER_ENABLE_REGISTRATION = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}