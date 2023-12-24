from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser
from pathlib import Path

configPath = Path(__file__).parent.parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(configPath)

# Get infos for Database-Connection
host = config["DATABASE"]["host"]
user = config["DATABASE"]["user"]
password = config["DATABASE"]["password"]
database = config["DATABASE"]["database"]

ssl_args = {
    "ssl": {
        "ca":  Path(__file__).parent.absolute() / "certs" / "ca-cert.pem",
        "cert": Path(__file__).parent.absolute() / "certs" / "client-cert.pem",
        "key": Path(__file__).parent.absolute() / "certs" / "client-key.pem",
        "check_hostname": False,
    }
}

SQLALCHEMY_DATABASE_URL = (
    f"mariadb+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=ssl_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()