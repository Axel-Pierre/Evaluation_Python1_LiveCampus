
import sqlite3
import requests
import csv
import psycopg2
import uuid
from bs4 import BeautifulSoup as bs
from psycopg2.extras import execute_values
import time
class Series:
    def __init__(self, url):
        self.url = url

    def recup(self):
        
        res = requests.get(self.url)
        soup = bs(res.text, 'html.parser')
        data = []
       
        entetes = ['name','epi_num','saison','date','country','channel','url']
        ##tables = soup.find(id ="calendrier").find_all('table',class_="padding2")[1]
        tables = soup.find_all('td',class_="td_jour")
        for select in tables : 
             list_epi =select.find_all('span', class_="calendrier_episodes")
             for episode in list_epi :
                  episode_name = episode.find_all('a')[0].text
                  episode_num = episode.find_all('a')[1].text.split('.')[1]
                  saison = episode.find_all('a')[1].text.split('.')[0]
                  date = episode.find_all('a')[1].get('href').split('-')[2]
                  episode_url = episode.find_all('a')[1].get('href')
                  country = episode.find_previous_sibling().find_previous_sibling()['alt']
                  channel = episode.find_previous_sibling()['alt']
                  data.append({'name' : episode_name,'epi_num': episode_num,'saison' : saison, "date" : date,'country' : country,'channel' : channel, 'url' : episode_url})
                
            
        with open('./data/files/episodes.csv','w+',encoding="utf-8") as f: 
            writer = csv.DictWriter(f,fieldnames=entetes)
            writer.writerows(data)
            f.close()
             
        return data
        ##for episode in tables :
        ##    episode_name = episode
           ## episode_num = episode.find_all('a')[1].text.split('.')[1]
           ## saison = episode.find_all('a')[1].text.split('.')[0]
          ##  date = episode.find_all('a')[1].get('href').split('-')[2]
         ##   country = tables.find_all('a')[0].find_previous_sibling()
          ##  data.append({'name' : episode_name,'epi_num': episode_num,'saison' : saison, "date" : date,'country' : country })
       ##     return episode_name
        exit()     
       
        ##return epi_table
      
        return data   
            
        ##dfs = pd.read_html(res.text)
        ##return tables
        
class Insert:

    def create():
        URL_DB = "postgres://userlivecampus:userlivecampus@livecampusp-4776.postgresql.a.osc-fr1.scalingo-dbs.com:30898/livecampusp_4776?sslmode=prefer"
        conn = sqlite3.connect('data/database/database.db')    
        distant_conn = psycopg2.connect(URL_DB)
        # Création d'un curseur pour exécuter des commandes SQL
        cur = conn.cursor()
        cor = distant_conn.cursor()
        entetes = ['name','epi_num','saison','date','country','channel','url']
        # Définition du schéma de la table
        cor.execute('''
         CREATE TABLE IF NOT EXISTS episode (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        numero_episode INT,
        saison INT,
        date TEXT,
        pays TEXT,
        chaine TEXT,
        url TEXT                        
             )
                ''')
        cur.execute('''
         CREATE TABLE IF NOT EXISTS episode (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        numero_episode INT,
        saison INT,
        date TEXT,
        pays TEXT,
        chaine TEXT,
        url TEXT                        
             )
                ''')

        # Validation des modifications
        conn.commit()

        with open('./data/files/episodes.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            uuid.uuid4().hex
            i = 1
            for row in spamreader:
                if len(row) > 0 :
                    
                    data_to_insert = [(tuple(row)[0],tuple(row)[1],tuple(row)[2],tuple(row)[3],tuple(row)[4],tuple(row)[5],tuple(row)[6])]
                    data_to_insert_scalingo = [(i,tuple(row)[0],tuple(row)[1],tuple(row)[2],tuple(row)[3],tuple(row)[4],tuple(row)[5],tuple(row)[6])]
                    i+1
                    records_list_template = ','.join(['%s'] * len(data_to_insert))
                    cur.executemany("INSERT  OR REPLACE INTO episode (nom, numero_episode,saison,date,pays,chaine,url) VALUES (?, ?, ? , ?, ?, ?, ?)", data_to_insert)
                   # cor.executemany("INSERT INTO episode (nom, numero_episode,saison,date,pays,chaine,url) VALUES (?, ?, ? , ?, ?, ?, ?)", data_to_insert)
                  ##  insert_query = "INSERT INTO episode (nom, numero_episode,saison,date,pays,chaine,url) VALUES {}".format(records_list_template)
                   ## cor.execute(insert_query,data_to_insert)
                    execute_values(cor, "INSERT  INTO episode (id,nom, numero_episode,saison,date,pays,chaine,url) VALUES %s",data_to_insert_scalingo)
        conn.commit()
        distant_conn.commit()

        cur.close
        cor.close
        conn.close
        distant_conn.close

class Episode :

      def __init__(self, data):
        self.data = data

      def detail_episode(self):
        URL_DB = "postgres://livecampus:FOy3hYFBndhbEj7x2u68@livecampusp-4776.postgresql.a.osc-fr1.scalingo-dbs.com:30898/livecampusp_4776?sslmode=prefer"
        conn = sqlite3.connect('data/database/database.db')    
        distant_conn = psycopg2.connect(URL_DB)
        # Création d'un curseur pour exécuter des commandes SQL
        cur = conn.cursor()
        cor = distant_conn.cursor()
       

        # Validation des modifications
        conn.commit()
        datas =[]
        cor.execute('''
        DROP TABLE  duration''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS duration (
        id INTEGER PRIMARY KEY,
        episode_time TEXT,
        url TEXT,
        UNIQUE(id,url),
        FOREIGN KEY (url) REFERENCES episode(url)  
                    );                     
            ''')
        cor.execute('''
        CREATE TABLE IF NOT EXISTS duration (
        id INTEGER PRIMARY KEY,
        episode_time TEXT,
        url TEXT,
        UNIQUE(id,url))''')
        i = 1
        for data in self.data : 
            
            res = requests.get('https://www.spin-off.fr/'+data['url'])
            time.sleep(0.2)
            
            soup = bs(res.text, 'html.parser')
            tables = soup.find('div',class_="episode_infos_episode_format").text
            tables = tables.replace('\n','')
            tables = tables.replace('\t','')
            data_stalingo = [(i,tables,data['url'])]
            print(tables)
            cur.execute("INSERT OR IGNORE INTO duration (episode_time,url) VALUES (?,?)",[(tables),(data['url'])])
            #cor.execute("INSERT INTO duration (episode_time,url) VALUES (?,?)",[(tables),(data['url'])])
            execute_values(cor, "INSERT  INTO duration (id,episode_time,url) VALUES %s",data_stalingo)
            conn.commit()
            distant_conn.commit()
            i = i+1
           
          