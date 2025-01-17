from tornado.web import HTTPError
from gramex.http import BAD_REQUEST
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import xlrd
import datetime
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

def topCrimeYTD(data, handler): #YearToDate function for each precinct
  thing2=pd.DataFrame()
  thing2=data
  thing2 = thing2[['Crime Type', 'Year to Date 2020', 'precinct']]
  cols = list(thing2['Crime Type'].unique())
  top5precinctYear = pd.pivot_table(thing2, values='Year to Date 2020', index='precinct',columns='Crime Type')
  unwanted_Cols =['TOTAL']
  top5precinctYear.drop(columns=unwanted_Cols, inplace=True)
  top5precinctYear['val'] = top5precinctYear.max(axis=1)
  top5precinctYear['Max'] = top5precinctYear.idxmax(axis=1)
  top5precinctYear=top5precinctYear.reset_index()
  top5precinctYear=top5precinctYear[['val', 'Max','precinct']].sort_values(by=['val'], ascending=False)
  return top5precinctYear


def topCrimeWTD(data, handler):#WeekToDate function for each precinct
  thing1=data
  thing1 = thing1[['Crime Type', 'Week to Date 2020', 'precinct']]
  cols = list(thing1['Crime Type'].unique())
  top5precinct = pd.pivot_table(thing1, values='Week to Date 2020', index=['precinct'], columns=['Crime Type'])
  unwanted_Cols =['TOTAL']
  top5precinct.drop(columns=unwanted_Cols, inplace=True)
  top5precinct['val'] = top5precinct.max(axis=1)
  top5precinct['Max'] = top5precinct.idxmax(axis=1)
  top5precinct=top5precinct.reset_index()
  top5precinct=top5precinct[['val', 'Max','precinct' ]].sort_values(by=['val'], ascending=False)
  return top5precinct


def topCrimeMTD(data, handler):#MonthToDate function for each precinct
  thing1=data
  thing1 = thing1[['Crime Type', '28 day 2020', 'precinct']]
  cols = list(thing1['Crime Type'].unique())
  top5precinct = pd.pivot_table(thing1, values='28 day 2020', index=['precinct'], columns=['Crime Type'])
  unwanted_Cols =['TOTAL']
  top5precinct.drop(columns=unwanted_Cols, inplace=True)
  top5precinct['val'] = top5precinct.max(axis=1)
  top5precinct['Max'] = top5precinct.idxmax(axis=1)
  top5precinct=top5precinct.reset_index()
  top5precinct=top5precinct[['val', 'Max','precinct' ]].sort_values(by=['val'], ascending=False)
  return top5precinct

def Crime2YrPerChange(data, handler):#MonthToDate function for each precinct
  thing3=data
  thing3 = thing3[['Crime Type', '2Yr %Chg', 'precinct']]
  thing3=thing3.replace(to_replace ="***.*", value =0.0)
  thing3['2Yr %Chg'] = thing3['2Yr %Chg'].astype(float) 
  thing3 = pd.pivot_table(thing3, values='2Yr %Chg', index=['precinct'],columns=['Crime Type'])
  unwanted_Cols =['TOTAL']
  thing3.drop(columns=unwanted_Cols, inplace=True)
  thing3['top5CrimeByPrec_2YRCHG'] = thing3.max(axis=1)
  thing3['Max'] = thing3.idxmax(axis=1)
  thing3=thing3.reset_index()
  thing3=thing3[['top5CrimeByPrec_2YRCHG', 'Max', 'precinct']].sort_values(by=['top5CrimeByPrec_2YRCHG'], ascending=False)
  return thing3

def Crime10YrPerChange(data, handler):#MonthToDate function for each precinct
  thing3=data
  thing3 = thing3[['Crime Type', '10Yr %Chg', 'precinct']]
  thing3=thing3.replace(to_replace ="***.*", value =0.0)
  thing3['10Yr %Chg'] = thing3['10Yr %Chg'].astype(float) 
  thing3 = pd.pivot_table(thing3, values='10Yr %Chg', index=['precinct'],columns=['Crime Type'])
  unwanted_Cols =['TOTAL']
  thing3.drop(columns=unwanted_Cols, inplace=True)
  thing3['top5CrimeByPrec_10YRCHG'] = thing3.max(axis=1)
  thing3['Max'] = thing3.idxmax(axis=1)
  thing3=thing3.reset_index()
  thing3=thing3[['top5CrimeByPrec_10YRCHG', 'Max', 'precinct']].sort_values(by=['top5CrimeByPrec_10YRCHG'], ascending=False)
  return thing3



def Crime27YrPerChange(data, handler):#MonthToDate function for each precinct
  thing3=data
  thing3 = thing3[['Crime Type', '27Yr %Chg', 'precinct']]
  thing3=thing3.replace(to_replace ="***.*", value =0.0)
  thing3['27Yr %Chg'] = thing3['27Yr %Chg'].astype(float) 
  thing3 = pd.pivot_table(thing3, values='27Yr %Chg', index=['precinct'],columns=['Crime Type'])
  unwanted_Cols =['TOTAL']
  thing3.drop(columns=unwanted_Cols, inplace=True)
  thing3['top5CrimeByPrec_27YRCHG'] = thing3.max(axis=1)
  thing3['Max'] = thing3.idxmax(axis=1)
  thing3=thing3.reset_index()
  thing3=thing3[['top5CrimeByPrec_27YRCHG', 'Max', 'precinct']].sort_values(by=['top5CrimeByPrec_27YRCHG'], ascending=False)
  return thing3

thisdict = {'40':"Bronx",'41':"Bronx",'42':"Bronx",'43':"Bronx",'44':"Bronx",'45':"Bronx",'46':"Bronx",'47':"Bronx",'48':"Bronx",'49':"Bronx",'50':"Bronx",'52':"Bronx",
  '60':"PB Brooklyn South",'61':"PB Brooklyn South",'62':"PB Brooklyn South",'63':"PB Brooklyn South",'66':"PB Brooklyn South",'67':"PB Brooklyn South",'68':"PB Brooklyn South",'69':"PB Brooklyn South",'70':"PB Brooklyn South",'71':"PB Brooklyn South",'72':"PB Brooklyn South",'76':"PB Brooklyn South",'78':"PB Brooklyn South",
  '73': "PB Brooklyn North",'75': "PB Brooklyn North",'77': "PB Brooklyn North",'79': "PB Brooklyn North",'81': "PB Brooklyn North",'83': "PB Brooklyn North",'84': "PB Brooklyn North",'88': "PB Brooklyn North",'90': "PB Brooklyn North",'94': "PB Brooklyn North",
  '1':"PB Manhattan South",'5':"PB Manhattan South",'6':"PB Manhattan South",'7':"PB Manhattan South",'9':"PB Manhattan South",'10':"PB Manhattan South",'13':"PB Manhattan South",'Midtown':"PB Manhattan South", '17':"PB Manhattan South", 'Midtown':"PB Manhattan South",
  '19':"PB Manhattan North",'20':"PB Manhattan North", 'Central':"PB Manhattan North", '23':"PB Manhattan North",'24':"PB Manhattan North",'25':"PB Manhattan North",'26':"PB Manhattan North",'28':"PB Manhattan North",'30':"PB Manhattan North",'32':"PB Manhattan North",'33':"PB Manhattan North",'34':"PB Manhattan North",
  '100':"PB Queens South",'101':"PB Queens South",'102':"PB Queens South",'103':"PB Queens South",'105':"PB Queens South",'106':"PB Queens South",'107':"PB Queens South",'113':"PB Queens South",
  '104':"PB Queens North",'108':"PB Queens North",'109':"PB Queens North",'110':"PB Queens North",'111':"PB Queens North",'112':"PB Queens North",'114':"PB Queens North",'115':"PB Queens North",
  '120':"PB Staten Island",'121':"PB Staten Island",'122':"PB Staten Island",'123':"PB Staten Island"}
