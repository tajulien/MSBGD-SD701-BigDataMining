import time
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import mysql.connector
import tokened

########################################################################################################################
# Initialization
########################################################################################################################
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',13)
DEBUG = True
date1 = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
DEBUG_FILE = fr'{os.getcwd()}/debug/result_scan-{date1}'
VISIBILITY_ERROR = []
########################################################################################################################
# global var
########################################################################################################################
YEARS = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
MONTHS = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre',
           'decembre']


########################################################################################################################
# Loading datas
########################################################################################################################
def loading_datas(year, month):
    try:
        connection = mysql.connector.connect(host=tokened.bddip,
                                             port=tokened.bddport,
                                             user=tokened.bdduser,
                                             password=tokened.bddpassword,
                                             database='sd701')

        sql_select_Query = f"SELECT * FROM `weather_datas` WHERE `unique_id` LIKE '{year}{month}%'"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        df = pd.DataFrame(records)
        df.columns = ['unique_id', 'date', 'heure', 'temp', 'pluie', 'vent', 'rafale', 'humidite', 'ressenti',
                     'radiation', 'pt_rose', 'pression', 'visibilite']
        if DEBUG:
            print(df.head(5))

        return df
    except Error as e:
        if DEBUG:
            print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


########################################################################################################################
# Check functions
########################################################################################################################
def checking_temp(datas):
    index_errors = []
    for i, item in enumerate(datas['temp']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Temperature are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in temperature, this dataframe needs to be fixed!')
        return False


def checking_rain(datas):
    index_errors = []
    for i, item in enumerate(datas['pluie']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Rain are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in rain, this dataframe needs to be fixed!')
        return False


def checking_wind(datas):
    index_errors = []
    for i, item in enumerate(datas['vent']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Wind are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in wind, this dataframe needs to be fixed!')
        return False


def checking_storm(datas):
    index_errors = []
    for i, item in enumerate(datas['rafale']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Storm are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in storm, this dataframe needs to be fixed!')
        return False


def checking_humidity(datas):
    index_errors = []
    for i, item in enumerate(datas['humidite']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Humidity are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in humidity, this dataframe needs to be fixed!')
        return False


def checking_feeling(datas):
    index_errors = []
    for i, item in enumerate(datas['ressenti']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Temp felt are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in temp felt, this dataframe needs to be fixed!')
        return False


def checking_radiation(datas):
    index_errors = []
    for i, item in enumerate(datas['radiation']):
        try:
            int(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Radiations are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in radiations, this dataframe needs to be fixed!')
        return False


def checking_rose(datas):
    index_errors = []
    for i, item in enumerate(datas['pt_rose']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Dew points are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in dew points, this dataframe needs to be fixed!')
        return False


def checking_pressure(datas):
    index_errors = []
    for i, item in enumerate(datas['pression']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.loc[[i]])
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Pressure are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in pressure, this dataframe needs to be fixed!')
        return False


def checking_visibility(datas):
    index_errors = []
    for i, item in enumerate(datas['visibilite']):
        try:
            float(item)
        except ValueError:
            if item == 'NaN':
                pass
            else:
                if DEBUG:
                    with open(DEBUG_FILE, 'a+') as f:
                        f.write('ERROR at index {}: {!r}\n'.format(i, item))
                        f.write(str(datas.loc[[i]]))
                        f.write('\n')
                    print('ERROR at index {}: {!r}'.format(i, item))
                    print(datas.unique_id.loc[[i]])
                    with open('visibility_errors.txt', 'a+') as fd:
                        fd.write(datas.unique_id.loc[[i]].values[0])
                        fd.write('\n')
                index_errors.append(i)
    if not index_errors:
        if DEBUG:
            print(f'Visibility are OK in this dataframe')
        return True
    else:
        if DEBUG:
            print(f'There are {len(index_errors)} errors in Visibility, this dataframe needs to be fixed!')
        return False


########################################################################################################################
# Result
########################################################################################################################
def checking_datas(datas):
    check = [checking_temp(datas), checking_rain(datas), checking_wind(datas), checking_storm(datas),
             checking_humidity(datas), checking_feeling(datas), checking_radiation(datas), checking_rose(datas),
             checking_pressure(datas), checking_visibility(datas)]
    print(check)
    if False in check:
        print(f'There are errors, this dataframe needs to be fixed!')
    else:
        print(f'Good job boy, all clean !')


def validate_datas(year, month):
    datas = loading_datas(year, month)
    checking_datas(datas)


for year in YEARS:
    for month in MONTHS:
        validate_datas(year, month)

## Too many visibility errors, got to improve my parsing algorithm and then update the database