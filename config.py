# the default application context
class Config(object):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///should_i_buy_it.db'
	SECRET_KEY = 'secret_key'

class InitialisingConfig(Config):
	RELOAD_DB = True
