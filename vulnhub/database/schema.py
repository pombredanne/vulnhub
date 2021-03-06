"""Schema

    Schema for NVD CVEs and CPEs in the database.
"""
import json
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, INTEGER, String, DateTime, FLOAT, TEXT
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine.url import URL
from sqlalchemy.pool import SingletonThreadPool


# Instantiate declarative base
DeclarativeBase = declarative_base()


def db_connect():
    """
    Connect to Database with configuration from Configuration file on disk
    Returns a connection and a metadata object
    :return: Database Connection instance with a pool_size=500, poolclass=SingletonThreaPool type
    """
    config_file = os.path.expanduser('~') + '/.vulnhub/dbconfig.json'
    # Fetch Database Settings
    with open(config_file) as config:
        config_data = json.load(config)
    return create_engine(URL(**config_data['DATABASE']), pool_size=500, poolclass=SingletonThreadPool)



def create_nvd_tables(engine):
    """
    Create tables with a postgres connection for NVD Database
    :param engine:
    :return:
    """
    DeclarativeBase.metadata.create_all(engine)


class CpeItem(DeclarativeBase):
    """Sqlalchemy model for NVD CPEs"""
    __tablename__ = "CpeItem"

    id = Column(INTEGER, primary_key=True)
    # CPE version 2.2 - CVE CPE relation
    cpeid = Column("cpeid", String, unique=True, nullable=False)

    # Text description of CPE URI
    cpetext = Column('cpetext', String, nullable=True)

    # CPE version 2.3 for backward compatibility relationship
    cpe_2_3 = Column('cpe_2_3', String, nullable=False)
    classification = Column('classification', String, nullable=True)

    # CPE Vendor Product Version
    vendor = Column('vendor', String, nullable=False)
    product = Column('product', String, nullable=False)
    version = Column('version', String, nullable=False)

    # CPE URI - Changelog reference from Vendor
    product_ref = Column('product_ref', String, nullable=True)


class CveItem(DeclarativeBase):
    """Sqlalchemy model for NVD CPEs"""
    __tablename__ = "CveItem"

    id = Column(INTEGER, primary_key=True)
    cve_id = Column("cveid", String, unique=True, nullable=False)
    software_list = Column("software_list", ARRAY(String, dimensions=1), nullable=False)
    published_date = Column("published_date", DateTime)
    modified_date = Column("modified_date", DateTime)
    Base_Score = Column("base_score", FLOAT)
    Base_Access_Vector = Column("access_vector", String)
    Base_Access_Complexity = Column("access_complexity", String)
    Base_Authentication = Column("Authentication", String)
    Base_Confidentiality_Impact = Column("confidentiality_impact", String)
    Base_Integrity_Impact = Column("integrity_impact", String)
    Base_Availability_Impact = Column("availability_impact", String)
    Base_Source = Column("source", String)
    Base_generation = Column("base_generation_date", DateTime)
    cwe_id = Column("cwe_id", ARRAY(String, dimensions=1))
    vulnerability_source = Column("vulnerability_source", ARRAY(String, dimensions=1))
    vulnerability_source_reference = Column("vulnerability_source_reference", ARRAY(String, dimensions=1))
    summary = Column("summary", TEXT)
