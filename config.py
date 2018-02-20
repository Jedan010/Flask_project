import os
basedir = os.getcwd()

class Config:
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '547054738@qq.com'
    MAIL_PASSWORD = 'ovmfsebwghkkbfcg'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Jedan]'
    FLASKY_MAIL_SENDER = 'Jedan Admin <547054738@qq.com>'
    FLASKY_ADMIN = 'jedan.wjd@foxmail.com'

    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        # 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    pass
    
config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig,

    'default': DevelopmentConfig
}
