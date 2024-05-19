# the default application context
class Config(object):
	SQLALCHEMY_DATABASE_URI = 'sqlite:///should_i_buy_it.db'
	SECRET_KEY = 'secret_key'
	UPLOAD_FOLDER =	"static\images"
	IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

	# session expiry timer (in hours)
	SESSION_EXPIRY = 18


class InitialisingConfig(Config):
	RELOAD_DB = True


class DevelopmentConfig(Config):
	"""Development configuration."""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///should_i_buy_it.db'


class TestingConfig(Config):
	"""Testing configuration."""
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
