class Config:
    SECRET_KEY = '#ensembl-technical-test#'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://anonymous@ensembldb.ensembl.org/ensembl_website_102'
