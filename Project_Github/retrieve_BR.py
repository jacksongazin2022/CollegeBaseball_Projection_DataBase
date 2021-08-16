"""
Author: Jackson Gazin
Baseball_Project
File: retrieve_BR
This file will retrieve the baseball reference key for each player name
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import urllib.request
pd.options.mode.chained_assignment = None
from urllib.parse import quote
from googlesearch import search
from bs4 import BeautifulSoup as bs

import csv
import requests

def get_BR_list(URL):
    #url = 'https://raw.githubusercontent.com/chadwickbureau/register/master/data/people.csv'
    response = requests.get(url)
    with open('out.csv', 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))
def get_BR_Dic(BR_database):
    BR_database['full_name'] = BR_database['name_first'].str.cat(BR_database['name_last'],sep="_")
    BR_database = BR_database.filter(['full_name','key_bbref_minors'])
    key_dic = dict(zip(list(BR_database['full_name']), list(BR_database['key_bbref_minors'])))
    return key_dic
def bref(database, BR_dic):
    list1 = []
    #database['full_name'] = database['firstName'].str.cat(database['lastName'],sep="_")
    name_list = database['full_name'].to_list()
    for i in range(len(name_list)):
        test = name_list[i]
        print(test)
        check =  BR_dic.get(test, None)
        if check != None:
            r = requests.get('https://www.baseball-reference.com/register/player.fcgi?id=' + str(check))
        if  check!= None and ('of the 2014 MLB June Amateur Draft' in r.text or 'of the 2015 MLB June Amateur Draft'\
            in r.text or 'of the 2016 MLB June Amateur Draft' in r.text or 'of the 2017 MLB June Amateur Draft' in
            \'r.text or 'of the 2018 MLB June Amateur Draft' in r.text):
            list1.append(check)
            print(check)
        else:
            test = test.replace("_", " ")
            query = test + " baseball reference minor league stats"
            for j in search(query,  tld='com', lang='en', num=1, start=0, stop=10, pause=2.0):
                if ".fcgi?id" in j:
                    check = j.split('=')[1]
                    r = requests.get('https://www.baseball-reference.com/register/player.fcgi?id=' + str(check))
                    if 'of the 2014 MLB June Amateur Draft' in r.text:
                        print(check + 'year' )
                        list1.append(check)
                        break
                    elif 'of the 2015 MLB June Amateur Draft' in r.text:
                        print(check + 'year')
                        list1.append(check)
                        break
                    elif 'of the 2016 MLB June Amateur Draft' in r.text:
                        print(check +  'year')
                        list1.append(check)
                        break
                    elif 'of the 2016 MLB June Amateur Draft' in r.text:
                        list1.append(check + 'year')
                        break
                        print(check + '2016')
                    elif 'of the 2017 MLB June Amateur Draft' in r.text:
                        list1.append(check)
                        break
                        print(check + '2017')
                    elif 'of the 2017 MLB June Amateur Draft' in r.text:
                        list1.append(check)
                        print(check + '2018')
                        break
                else:
                    next
    database['BR_Key'] = list1
    return(database)
        


