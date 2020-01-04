from bs4 import BeautifulSoup
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver import Chrome

import pandas as pd

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



def get_dropping_odds():
    '''
    makes a dataframe from the oddsportal dropping odds main page
    '''
    
    url = "https://www.oddsportal.com/dropping-odds/"
    webdriver_path = "driver/chromedriver"
    browser = Chrome(webdriver_path)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, features="lxml")
    game_table = soup.findAll('table', {'class': 'table-main'}) # find the table
    
    # process and transform with pandas
    game_table = pd.read_html(str(game_table), header=0)[0]
    game_table.columns = ['time','teams','drop1','drop2','drop3','drop4','drop5']
    cond1 = game_table['drop1'].str.contains('%')
    cond2 = game_table['drop2'].str.contains('%')
    cond3 = game_table['drop3'].str.contains('%')
    cond4 = game_table['drop4'].str.contains('%')
    cond5 = game_table['drop5'].str.contains('%')
    df = game_table[(cond1 | cond2 | cond3 | cond4 | cond5)]

    for index,row in df.iterrows():

        if '%' in row['drop1']:
            value = -int(row['drop1'][1:3])  
            df.loc[index, 'drop'] = value

        elif '%' in row['drop2']:
            value = -int(row['drop2'][1:3])  
            df.loc[index, 'drop'] = value

        elif '%' in row['drop3']:
            value = -int(row['drop3'][1:3])  
            df.loc[index, 'drop'] = value 

        elif '%' in row['drop4']:
            value = -int(row['drop4'][1:3])  
            df.loc[index, 'drop'] = value

        elif '%' in row['drop5']:
            value = -int(row['drop5'][1:3])  
            df.loc[index, 'drop'] = value

        else:
            df.loc[index, 'drop'] = None

    df.drop(['drop1','drop2','drop3','drop4','drop5'], axis=1, inplace=True)
    
    cond = df['drop'] <= -20
    df = df[cond]
    
    return df
    