"""
This module is used to add csv file data to database and
perform crud operations on it using defined methods.
Database name should be passed in configuration and
for CRUD operations tablename is common parameter
which is returned from create_record() method.
"""
__author__ = "Snehal Borkar"
__email__ = "borkarsnehal60.com"
__status__ = "planning"

import logging
import re
import ntpath
import mysql.connector
from pandas import read_csv

logger = logging.getLogger()


def connect_db(configure):
    """
    connects to the database for performing crud
    :param configure: is dictionary of database credentials and database name
    :return: connection object.
    """
    try:
        connection = mysql.connector.connect(**configure)
        if connection.is_connected():
            logger.info("Successfully connected to %s database \
            at port %s", configure["database"], configure["port"])
    except mysql.connector.errors.ProgrammingError as ex:
        logger.error("%s : %s", ex.__class__.__name__, ex)
        raise mysql.connector.errors.ProgrammingError
    except KeyError as ex:
        logger.error("%s : %s is missing in database configuration", ex.__class__.__name__, ex)
        raise KeyError
    return connection


def clean(key):
    """Replace invalid characters with _"""
    clean_key = re.sub('[^0-9a-zA-Z_]', '_', key)
    logger.debug("successfully return from clean(%s) - %s", key, clean_key)
    return clean_key


def extract_csv_data(file_name):
    """
    Read csv file and preserve datatype of columns using pandas and
    extract column name list and values list
    :param file_name: csv filename or absolute file path to be read
    :return: column_name_dtype dict of dataframe column type to
    python type and  values_list list of tuples of values
    """

    dataframe = read_csv(file_name, keep_default_na=False)
    logger.info("Successfully read %s", file_name)
    # column_inf_dtype = [pd.api.types.infer_dtype(dataframe[i], skipna=True)
    #                     for i in dataframe.columns]
    # print("column_inf_dtype :",column_inf_dtype)
    column_name_dtype = dict(([(dataframe[x].name, dataframe[x].dtype.name) for x in dataframe]))
    for key, value in column_name_dtype.items():
        if value == "object":
            column_name_dtype[key] = "TEXT"
        elif value == "int64":
            column_name_dtype[key] = "BIGINT"
        elif value == "float64":
            column_name_dtype[key] = "DOUBLE"
        elif value == "bool":
            column_name_dtype[key] = "BOOLEAN"
        else:
            column_name_dtype[key] = "TEXT"
    values_list = list(map(tuple, dataframe.values.tolist()))
    logger.debug("Successfull return %s -- %s", column_name_dtype, values_list)
    return column_name_dtype, values_list


def create_record(filename, configure, internal_csv_file=True):
    """
    Create tablename in database in configure and add csv extracted data to database.
    :param filename: filename or absolute path of csv file to read.
    :param configure: Configuration of database with database name.
    :param internal_csv_file: if method is called from outside app value is False ex. for testing .
    :return: table name in which csv data is added.
    """
    connection = connect_db(configure)
    if internal_csv_file == True:
        internal_csv_file_name = "csv_file.csv"
    else:
        internal_csv_file_name = filename

    column_name_dtype, values_list = extract_csv_data(internal_csv_file_name)
    col_type_list = []
    value_holder_list = []
    count = 0
    pk_key_list = []
    for key, value in column_name_dtype.items():
        clean_key = clean(key)
        count += 1
        if count == 1 or count == 2 or count == 3:
            pk_key_list.append(clean_key)
            if value == "TEXT":
                value = "VARCHAR(255)"
            col_type = f"{clean_key} {value}"
        else:

            col_type = f"{clean_key} {value}"
        col_type_list.append(col_type)
        value_holder_list.append("%s")

    delimiter = ","
    pk_key_str = delimiter.join(map(str, pk_key_list))
    col_type_str = delimiter.join(map(str, col_type_list))
    value_holder_str = delimiter.join(map(str, value_holder_list))
    logger.debug("Successfully generated str,  %s -- %s -- %s", pk_key_str, col_type_str, value_holder_str)

    my_cursor = connection.cursor()

    def path_leaf(path):
        """
        extract root file name after / from absolute file path
        :param path: Absolute path of file
        :return: file name with .csv extension
        """
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    ext_file_name = path_leaf(filename)

    logger.debug("ext_file_name is  : %s and type is %s", ext_file_name, type(ext_file_name))
    root_table_name = clean((ext_file_name.split("."))[0])
    logger.debug("root_table_name : %s", root_table_name)
    table_name = root_table_name
    count = 0
    while True:
        try:
            sql = f"CREATE TABLE {table_name}({col_type_str},\
             CONSTRAINT PRIMARY KEY({pk_key_str}))"
            # print(sql)
            my_cursor.execute(sql)
            logger.info("Successfully created table '%s' at '%s' - \
            database", table_name, configure["database"])
            break
        except mysql.connector.errors.ProgrammingError:
            count += 1
            table_name = root_table_name + "_" + str(count)

    try:
        sql = f"INSERT INTO {table_name} VALUES({value_holder_str})"
        my_cursor.executemany(sql, values_list)
        logger.info("Successfully inserted rows in '%s'- table at '%s'- database", table_name, configure["database"])
    except mysql.connector.errors.ProgrammingError as ex:
        logger.error("%s : %s", ex.__class__.__name__, ex)
        raise mysql.connector.errors.ProgrammingError

    connection.commit()
    my_cursor.close()
    connection.close()
    return table_name


def show_data(table_name, configure):
    """
    Fetch all records from table to render in html page
    :param table_name: Table name from which records to be fetched
    :param configure: database configuration
    :return: field_names-column names of table, records- list of tuples
             of all records,pk_field_list- list of primary key fields,
             table_name- tablename from which data is fetched
    """
    connection = connect_db(configure)
    sql = f"SELECT * FROM {table_name}"
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    records = my_cursor.fetchall()
    # print(records)
    field_names = [i[0] for i in my_cursor.description]
    sql = f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'"
    try:
        my_cursor.execute(sql)
        logger.info("Successfully Read data from table '%s'", table_name)
    except mysql.connector.errors.ProgrammingError as ex:
        logger.error("%s : %s", ex.__class__.__name__, ex)
        raise mysql.connector.errors.ProgrammingError
    pk_fields_desc = my_cursor.fetchall()
    pk_field_list = []
    for pk in pk_fields_desc:
        pk_field_list.append(pk[4])
    # print("pk_field_list :", pk_field_list)
    my_cursor.close()
    connection.close()
    logger.debug("returned_values from test_read_from_db_unsuccessful : %s -  %s - %s - %s", field_names, records,
                 pk_field_list, table_name)
    return field_names, records, pk_field_list, table_name


def delete_record(table_name, filter_condn, configure):
    """
    Delete record from the database for filter condition
    :param table_name: from row to delete
    :param filter_condn: condition at which row be delete
    :param configure: database configuration
    :return: tablename from which record is deleted
    """
    connection = connect_db(configure)
    sql = f"DELETE FROM {table_name} WHERE {filter_condn}"
    print(sql)
    my_cursor = connection.cursor()
    try:
        my_cursor.execute(sql)
        logger.info("Successfully Deleted data from table '%s' at conditions %s ", table_name, filter_condn)
    except mysql.connector.errors.ProgrammingError as ex:
        logger.error("%s : %s", ex.__class__.__name__, ex)
        print(ex.__class__.__name__, ex)
        raise mysql.connector.errors.ProgrammingError
    connection.commit()
    my_cursor.close()
    connection.close()
    return table_name


def update_form_fill(table_name, filter_condn, configure):
    """
    Fetch data from database for condition whose row is to be render in update form to edit
    :param table_name: from which data be fetching
    :param filter_condn: condition for row to select
    :param configure: datbase configuration
    :return: record_dict-dictionary of column:record value, table_name, filter_condn
    """
    connection = connect_db(configure)
    sql = f"SELECT * FROM {table_name} WHERE {filter_condn}"
    # print(sql)
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    records = my_cursor.fetchall()
    field_names = [i[0] for i in my_cursor.description]
    record_dict = {}
    for i in range(len(field_names)):
        record_dict.update({field_names[i]: records[0][i]})
        # print(record_dict)
    return record_dict, table_name, filter_condn


def update(table_name, update_set_str, filter_str, configure):
    """
    Update table row for received SET values and condition
    :param table_name: tablename in which update be performing
    :param update_set_str: column and values be updating
    :param filter_str: condition at which update be performing
    :param configure: database configuration
    :return: Database error message for unsuccess operation
    """
    connection = connect_db(configure)
    # print(update_SET_str)
    sql = f"UPDATE  {table_name} SET {update_set_str} WHERE  {filter_str}"
    # print("Update Sql :",sql)
    my_cursor = connection.cursor()
    try:
        my_cursor.execute(sql)
    except mysql.connector.errors.DatabaseError as ex:
        logger.debug("%s - %s", ex.__class__.__name__, ex)
        return ex.msg

    connection.commit()
    my_cursor.close()
    connection.close()


def add(table_name, configure, fields=None):
    """
     add new row to database table.
    :param table_name: tablename to which create be performing
    :param configure: database configuration
    :param fields: fields to creating ,None if rendering only create form
    :return: Database error message for unsuccess operation
    """
    connection = connect_db(configure)
    sql = f"SELECT * FROM {table_name}"
    # print(sql)
    my_cursor = connection.cursor()
    my_cursor.execute(sql)
    my_cursor.fetchall()
    field_names = [i[0] for i in my_cursor.description]
    # print(field_names)
    if not fields:
        return field_names

    # print("fields from add form:", fields)
    field_values_list = []
    # print(fields)
    for key in field_names:
        if len(fields[key][0]) == 0:
            data = 'NULL'
        else:
            inv_comma_include_str = ''
            for i_c in range(len(fields[key][0])):
                if fields[key][0][i_c] == '"':
                    inv_comma_include_str += '""'
                else:
                    inv_comma_include_str += fields[key][0][i_c]
            data = f'"{inv_comma_include_str}"'
        field_values_list.append(data)
    delimiter = ","
    field_values_str = (delimiter.join(map(str, tuple(field_values_list))))
    sql = f"INSERT INTO  {table_name} VALUES({field_values_str})"
    # print("sql :",sql)
    my_cursor = connection.cursor()
    try:
        my_cursor.execute(sql)
    except mysql.connector.errors.DatabaseError as ex:
        logger.debug("%s - %s", ex.__class__.__name__, ex)
        return ex.msg
    connection.commit()
    my_cursor.close()
    connection.close()
