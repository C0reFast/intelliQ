#!/usr/bin/env python
# encoding: utf-8

from pony.orm import *
import config

db = Database("mysql",
              host=config.db_host,
              user=config.db_user,
              passwd=config.db_password,
              db=config.db_database)


class Company(db.Entity):
        _table_ = "company"
        company_id = PrimaryKey(int, auto=True)
        company_name = Required(unicode)
        search_exp = Required(unicode, 500)


sql_debug(True)
db.generate_mapping(create_tables=True)
