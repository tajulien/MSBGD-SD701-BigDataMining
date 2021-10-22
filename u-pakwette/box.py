import os

import json
import re
import time
from datetime import datetime

import requests
import tokened
import mysql.connector

from mysql.connector import Error
from bs4 import BeautifulSoup
from calendar import monthrange

# dates to check from 01/01/2013 to 20/10/2021
# site format : 19/octobre/2021/paris-montsouris/07156.html
# let's divide in multiples splits to avoid blocked connection from the remote site
get_all_days = {}
get_all_day_num_month = {}
years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
# months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre',
#           'decembre']
months = ['mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre',
          'decembre']

for year in years:
    get_all_days[year] = {}

for year in years:
    get_all_days[year] = {}
    for month in months:
        get_all_days[year][month] = monthrange(year, months.index(month) + 1)[1]


def get_parsed_page(url):
    headers = {
        "referer": "https://www.infoclimat.fr/observations-meteo/archives/4/aout/2021/paris-montsouris/07156.html",
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")


def get_the_page(yir, montz, day):
    data_day = {}
    link = f'https://www.infoclimat.fr/observations-meteo/archives/{day}/{montz}/{yir}/paris-montsouris/07156.html'
    print(link)
    home = get_parsed_page(link)
    tr_elements = home.find_all('table')[2].find_all('tr')
    tr_elements = [str(tr) for tr in tr_elements]

    ####################################################################################################################
    # Count number of hours
    ####################################################################################################################
    iteration = len(tr_elements) - 1
    for i in range(1, iteration + 1):
        print(tr_elements[i])
        ################################################################################################################
        # Heure
        ################################################################################################################
        tags_heure = 'UTC&lt;/b&gt;">'
        if tr_elements[i].find(tags_heure) != -1:
            heure = tr_elements[i][tr_elements[i].find(tags_heure) + len(tags_heure):]
            heure = heure[:heure.find("<")].strip(' ')
        else:
            heure = "NaN"

        ################################################################################################################
        # Temperature
        ################################################################################################################
        tags_temp = '/div&gt;\">'
        if tr_elements[i].find(tags_temp) != -1:
            temp = tr_elements[i][tr_elements[i].find(tags_temp) + len(tags_temp):]
            temp = temp[:temp.find("<")].strip(' ')
        else:
            temp = "NaN"
        ################################################################################################################
        # Précipitations
        ################################################################################################################

        tags_precip = '</td><td>'
        if tr_elements[i].find(tags_precip) != -1:
            precip = tr_elements[i][tr_elements[i].find(tags_precip) + len(tags_precip):]
            precip = precip[:precip.find("<")]
            if len(precip) > 6 or precip == '' or precip=='\n':
                tags_precip = 'minutes.\">'
                precip = tr_elements[i][tr_elements[i].find(tags_precip) + len(tags_precip):]
                precip = precip[:precip.find("<")].strip(' ')
                if len(precip) > 6:
                    tags_precip= "<span class=\"tab-units-v\">mm/1h"
                    precip = tr_elements[i][tr_elements[i].find(tags_precip)-5:]
                    precip = precip[precip.find(">"):]
                    precip = precip[1:precip.find("<")].strip(' ')
        else:
            precip = "NaN"
        ################################################################################################################
        # Vitesse vent
        ################################################################################################################
        tags_vent = 'style="font-weight:bold">'
        if tr_elements[i].find(tags_vent) != -1:
            vent = tr_elements[i][tr_elements[i].find(tags_vent) + len(tags_vent):]
            vent = vent[:vent.find("<")].strip(' ')
        else:
            vent = "NaN"

        ################################################################################################################
        # Vitesse rafales
        ################################################################################################################
        tags_rafales = 'raf.</span><span style="font-weight:bold">'
        if tr_elements[i].find(tags_rafales) != -1:
            rafales = tr_elements[i][tr_elements[i].find(tags_rafales) + len(tags_rafales):]
            rafales = rafales[:rafales.find("<")].strip(' ')
        else:
            rafales = "NaN"

        ################################################################################################################
        # Humidité
        ################################################################################################################
        tags_hum = 'font-weight:bold;display:inline-block">'
        if tr_elements[i].find(tags_hum) != -1:
            hum = tr_elements[i][tr_elements[i].find(tags_hum) + len(tags_hum):]
            hum = hum[:hum.find("<")].strip(' ')
        else:
            hum = "NaN"

        ################################################################################################################
        # Temp ressentie
        ################################################################################################################
        tags_t_res = '<span style="display:inline-block">'
        if tr_elements[i].find(tags_t_res) != -1:
            t_res = tr_elements[i][tr_elements[i].find(tags_t_res) + len(tags_t_res):]
            t_res = t_res[:t_res.find("<")].strip(' ')
        else:
            t_res = "NaN"

        ################################################################################################################
        # Radiations
        ################################################################################################################
        tags_rad = '"Radiations Solaires mesurées (W/m²)"><span class="">'
        if tr_elements[i].find(tags_rad) != -1:
            rad = tr_elements[i][tr_elements[i].find(tags_rad) + len(tags_rad):]
            rad = rad[:rad.find("<")].strip(' ')
        else:
            rad = "NaN"
        ################################################################################################################
        # Point de rosé
        ################################################################################################################
        tags_rose = 'style="font-weight:bold;display:inline-block">'
        if tr_elements[i].find(tags_rose) != -1:
            pos_rose = tr_elements[i].find(tags_rose)
            rose = tr_elements[i][tr_elements[i].find(tags_rose, pos_rose + 1) + len(tags_rose):]
            rose = rose[:rose.find("<")].strip(' ')
        else:
            rose = "NaN"

        ################################################################################################################
        # Pression
        ################################################################################################################
        tags_pression = '<span class="tab-units-v">hPa'
        if tr_elements[i].find(tags_pression) != -1:
            pression = tr_elements[i][:tr_elements[i].find(tags_pression)]
            pression = pression[-6:].strip(' ')
            pression = re.sub(r'\b[^\d\W]+\b>', '', pression)
        else:
            pression = "NaN"

        ################################################################################################################
        # Visibilité
        ################################################################################################################
        tags_visi = '<td style="/*background-color:rgba(0,0,0,0.1)*/">'
        if tr_elements[i].find(tags_visi) != -1:
            visi = tr_elements[i][-150:]
            visi = visi[visi.find(tags_visi) + len(tags_visi):]
            visi = visi[:visi.find("<")].strip(' ')
        else:
            visi = "NaN"

        data_day[heure] = {"temp": temp, "precip": precip, "vent": vent, "rafales": rafales, "hum": hum, "t_res": t_res,
                           "rad": rad, "rose": rose, "pression": pression, "visi": visi}

    # print(data_day)

    with open(f'{os.getcwd()}/json/{yir}{montz}{day}.json', 'w+') as json_file:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        #print(f'{current_time} data printed')
        json.dump(data_day, json_file)
    if day == '1er':
        day = '1'
    if int(day) < 10:
        day = '0'+str(day)
    unique_id = str(yir) + str(montz) + str(day)

    return [data_day, unique_id]


totaladd = 0


def envoi_sql(record_to_insert):
    global totaladd
    try:
        connection = mysql.connector.connect(host=tokened.bddip,
                                             port=tokened.bddport,
                                             user=tokened.bdduser,
                                             password=tokened.bddpassword,
                                             database='sd701')

        sql_insert_query = """INSERT IGNORE INTO weather_datas (unique_id, date, heure, temp, pluie, vent, rafale, 
        humidite, ressenti, radiation, pt_rose, pression, visibilite) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s) """
        # ON DUPLICATE KEY UPDATE unique_id = %s, date=%s, heure=%s, temp=%s, pluie=%s, vent=%s, rafale=%s, humidite=%s,
        #          ressenti=%s, radiation=%s, pt_rose=%s, pression=%s, visibilite=%s
        cursor = connection.cursor(prepared=True)
        result = cursor.executemany(sql_insert_query, record_to_insert)
        connection.commit()
        totaladd += cursor.rowcount
        print(cursor.rowcount, f"Record inserted successfully into sd701 table - {totaladd}")
    except mysql.connector.Error as error:
        print("Failed inserting record into sd701 table {}".format(error))
    finally:
        print('Terminating')
        if connection.is_connected():
            cursor.close()
            connection.close()


SEND_SQL = True


def parse_master(year, month, day):
    one_test = get_the_page(year, month, day)
    record_to_insert = []
    for i in range(0, len(one_test[0])):

        e = months.index(month) + 1
        if day == '1er':
            day = "01"
        date = one_test[1][:4] + str(f'{e:02d}') + str(day)
        if f'{i:02d}h' in one_test[0].keys():
            touple = (one_test[1] + f'-{i:02d}', date, f'{i:02d}', one_test[0][f'{i:02d}h']['temp'],
                      one_test[0][f'{i:02d}h']['precip'], one_test[0][f'{i:02d}h']['vent'],
                      one_test[0][f'{i:02d}h']['rafales'], one_test[0][f'{i:02d}h']['hum'],
                      one_test[0][f'{i:02d}h']['t_res'], one_test[0][f'{i:02d}h']['rad'].replace(u'\xa0', u' '),
                      one_test[0][f'{i:02d}h']['rose'], one_test[0][f'{i:02d}h']['pression'],
                      one_test[0][f'{i:02d}h']['visi'])
            record_to_insert.append(touple)
    time.sleep(2)
    if SEND_SQL:
        envoi_sql(record_to_insert)



parse_master('2013', 'mars', '31')
