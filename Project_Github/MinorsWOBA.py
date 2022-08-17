"""
Author: Jackson Gazin
Baseball_Project
File: MinorsWOBA.py
Run this program after retrieving a key for each desired player. It will take the table which includes the first and last name
of the desired college baseball player along with their BBREF key and return their total Minor League WOBA.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import requests
import quandl


def return_key_list(database):
    return list(database['Ref_Key'])
def Pro_WOBA_Data_by_key(database,key_list):
    #create a list to append the WOBAs to
    list1 = []
    for i in range(len(key_list)):
        #try and except will allow the WOBA value to return NA if it is not calculatable (ex. page does not exist, table does no exist, pitcher stats, etc)
        try:
            #finds the URL based on the key, BAseball Ref urls for players will always follow this format
            
            URL = "https://www.baseball-reference.com/register/player.fcgi?id=" + key_list[i]
            
            #read all of the tables
            
            tables = pd.read_html(URL)

            #return the first table (only table for BR)
            tables = tables[0]
            
            #make our table equal to the row with minor league stats
            
            tables = tables.loc[tables.Year.str.contains("Minors", na=False)]

            #only need to retrieve columns that will be apart of the WOBA calculation
            tables = tables.filter(['H','2B','3B', 'HR', 'BB', 'IBB', 'HBP', 'SF', 'AB'], axis=1)

            #convert each column to a numeric
            tables = tables.apply(pd.to_numeric)

            #calculate singles
            
            tables['Single'] = tables['H'] - tables['2B'] - tables['3B'] - tables['HR']

            #calculate uBB (neccesary for WOBA calculation)
            
            tables['uBB'] = tables['BB'] - tables['IBB']
            
            #convert to numeric again
            
            tables = tables.apply(pd.to_numeric)

            #calculate WOBA
            
            tables['WOBA'] = (.69*tables['uBB'] + .72 * tables['HBP'] + .89 * tables['Single'] + 1.27 * tables['2B'] + 1.62 * tables['3B']\
                              + 2.10 * tables['HR'])/(tables['AB'] + tables['uBB'] + tables['SF'] + tables['HBP'])

            #append only the value of this WOBA)
            list1.append(tables['WOBA'].values[0])
        except:

            #if WOBA cannot be calculated just append NA
            list1.append('NA')
        i += 1
    database['MinorsWOBA'] = list1
    return database
    
    #try and except works perfectly because it will give the key a value of no table if it doesn't have a page OR IF IT IS A PITCHER

#new_file = Pro_WOBA_Data_by_key(data)




