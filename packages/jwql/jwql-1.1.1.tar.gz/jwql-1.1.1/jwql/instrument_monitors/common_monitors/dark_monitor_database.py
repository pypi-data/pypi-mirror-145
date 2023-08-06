#! /usr/bin/env python

"""Functions to help query and add content to the database associated with
the dark current monitor
"""




from sqlalchemy import Table

from jwql.database.database_interface import base
from jwql.database.database_interface import session
from jwql.database.database_interface import NircamDarkDarkCurrent

my_data = {}
my_data['column_name_1'] = 'foo'
my_data['column_name_2'] = 'bar'



def insert(table_name, data):
    # Check to see if a record already exists
    query = session.query(table_name)\
        .filter(table_name.some_value == some_other_value)
    query_count = query.count()

    # If there are no results, then perform an insert
    if not query_count:
        tab = Table('nircam_dark_dark_current', base.metadata, autoload=True)
        insert_obj = tab.insert()
        insert_obj.execute(my_data)

    # Otherwise, perform an update on the row
    else:
        query.update(my_data)