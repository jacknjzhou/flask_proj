# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, Query
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.pool import NullPool

from find_partner.config import DB_OSS_PARTNER_URL

engine = create_engine(DB_OSS_PARTNER_URL + '?charset=utf8',
                       encoding='utf-8',
                       convert_unicode=True,
                       poolclass=NullPool,
                       echo=False)


class CommonBase(object):
    def __init__(self, base):
        self.base = base
        self.Model = self.make_declarative_base()

    def make_declarative_base(self):
        base = declarative_base(cls=self.base)
        base.query_class = Query
        return base


class Base(object):
    @declared_attr
    def __table__(cls):
        return Table(cls.__tablename__, MetaData(), autoload=True, autoload_with=engine)


db = CommonBase(Base)


class TbCompanyCustomer(db.Model):
    __tablename__ = 'tb_company_customer'


class TbCompanyVendor(db.Model):
    __tablename__ = 'tb_company_vendor'


class TbConfCenterCompany(db.Model):
    __tablename__ = 'tb_conf_center_company'


create_partner_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
