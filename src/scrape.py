'''
Utilitaire pour extraire les données des notes NBA 2K de 2014 à 2023 à partir de hoopshype.com, et les sauvegarder dans un fichier CSV.
'''


import requests
import pandas as pd
from bs4 import BeautifulSoup

data = []

for saison in range(2014, 2024):
    url = f"https://hoopshype.com/nba2k/{saison}-{saison+1}/"

    # Requête de la page web avec les notes 2k
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to get data for saison {saison}-{saison+1}")
        continue

    # On utilise BeautifulSoup pour parser la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # ça tombe bien, il n'y a qu'un seul tableau sur la page qui contient les notes qu'on veut
    table = soup.find('table')

    # On récupère le contenu du tableau
    rows = table.find_all('tr')[1:]

    # On parcourt les lignes du tableau
    for row in rows:
        columns = row.find_all('td')
        player_name = columns[0].text.strip()
        team = columns[1].text.strip()
        rating = columns[2].text.strip()

        # On ajoute 1 à la saison pour obtenir l'édition du jeu (ex: 2014-2015 => 2015)
        data.append([saison+1, player_name, team, rating])
    df = pd.DataFrame(data, columns=['Season', 'Id', 'Player', 'Rating'])

    

df.to_csv('nba_2k_ratings_2014_to_2023.csv', index=False)
