class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iescpmaindatabase.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'Rituparnoinfluencersposorapp'
    SECURITY_PASSWORD_SALT = 'rituparnoinfluencerpasswordsalt'