from pro_football_reference_web_scraper import team_game_log as t
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from bs4 import BeautifulSoup
import requests


team_hrefs = {
    'Arizona Cardinals': 'crd',
    #'Baltimore Colts': 'clt',
    #'St. Louis Cardinals': 'crd',
    #'Boston Patriots': 'nwe',
    'Chicago Bears': 'chi',
    'Green Bay Packers': 'gnb',
    'New York Giants': 'nyg',
    'Detroit Lions': 'det',
    'Washington Commanders': 'was',
    #'Washington Football Team': 'was',
    #'Washington Redskins': 'was',
    'Philadelphia Eagles': 'phi',
    'Pittsburgh Steelers': 'pit',
    'Los Angeles Chargers': 'sdg',
    'San Francisco 49ers': 'sfo',
    #'Houston Oilers': 'oti',
    'Cleveland Browns': 'cle',
    'Indianapolis Colts': 'clt',
    'Dallas Cowboys': 'dal',
    'Kansas City Chiefs': 'kan',
    'Los Angeles Rams': 'ram',
    'Denver Broncos': 'den',
    'New York Jets': 'nyj',
    'New England Patriots': 'nwe',
    'Las Vegas Raiders': 'rai',
    'Tennessee Titans': 'oti',
    #'Tennessee Oilers': 'oti',
    #'Phoenix Cardinals': 'crd',
    #'Los Angeles Raiders': 'rai',
    'Buffalo Bills': 'buf',
    'Minnesota Vikings': 'min',
    'Atlanta Falcons': 'atl',
    'Miami Dolphins': 'mia',
    'New Orleans Saints': 'nor',
    'Cincinnati Bengals': 'cin',
    'Seattle Seahawks': 'sea',
    'Tampa Bay Buccaneers': 'tam',
    'Carolina Panthers': 'car',
    'Jacksonville Jaguars': 'jax',
    'Baltimore Ravens': 'rav',
    'Houston Texans': 'htx',
    #'Oakland Raiders': 'rai',
    #'San Diego Chargers': 'sdg',
    #'St. Louis Rams': 'ram',
    #'Boston Patriots': 'nwe',
}

seasons = [2022,2023]

Schedules = []
team_stats = []
print('Requesting Data...')
for season in seasons:
    for key, value in team_hrefs.items():
        print(season,' ',key,': ', value)
        url = f'https://www.pro-football-reference.com/teams/{value}/{season}.htm'
        tables = pd.read_html(url)
        stats = tables[0]
        stats['Season'] = season
        stats['Team'] = key
        team_stats.append(stats)
        schedule = tables[1]
        schedule['Season'] = season
        schedule['Team'] = key
        Schedules.append(schedule)
        time.sleep(3) # add delay to parser to not overload the requests
        
print('Cleaning Data...')
Schedules_cleaned = []
for df in Schedules:
    df.columns = df.columns.droplevel()
    df = df.rename(columns={'Unnamed: 3_level_1':'Time', 'Unnamed: 4_level_1':'Type',
        'Unnamed: 5_level_1':'Result', 'OT':'Overtime', 'Rec':'Record', 'Unnamed: 8_level_1':'Home/Away', 'Opp':'Oponent', 'Tm':'Points Scored',
        'Opp':'Opponent Points Scored', '1stD':'#1st Downs', '1stD':'Opp 1stD', 'TotYd': 'Opp TotYd',
        'PassY': 'Opp PassY', 'RushY':'Opp RushY', 'TO':'Opp TO', 'Offense':'Expected Offense', 'Defense':'Expected Defense', 'Sp. Tms':'Expected Special Team Points'})
    columns = df.columns.tolist()
    columns[-2] = 'Season'
    columns[-1] = 'Team'
    df.columns = columns
    Schedules_cleaned.append(df)
print(f'Done: {len(Schedules_cleaned)} DataFrames extracted!')
print('Combining data...')
All_games = pd.concat(Schedules_cleaned, axis=0)
All_games = All_games.reset_index(drop=True)
print(All_games.info())

All_games.to_csv('NFL_Games.csv')
