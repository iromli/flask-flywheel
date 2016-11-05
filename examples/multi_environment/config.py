

class Config(object):
    """Base configuration."""

    FLYWHEEL_DATABASE_HOST = "localhost"
    FLYWHEEL_DATABASE_PORT = 8000
    FLYWHEEL_SECURE = False
    SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'


class ProdConfig(Config):
    """Production configuration."""

    FLYWHEEL_ENGINE_NAMESPACE = "prod"


class StagingConfig(Config):
    """Production configuration."""

    FLYWHEEL_ENGINE_NAMESPACE = "staging"


class DevConfig(Config):
    """Development configuration."""

    FLYWHEEL_ENGINE_NAMESPACE = "dev"


class TestConfig(Config):
    """Test configuration."""

    DEBUG = True
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
