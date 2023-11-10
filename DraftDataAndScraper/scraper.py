import requests
from bs4 import BeautifulSoup
import csv

def scrape_nfl_draft(year):
    url = f"https://www.pro-football-reference.com/years/{year}/draft.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    drafted_players = []
    draft_table = soup.find_all('tr', class_='draft')  # Confirm this class name

    for row in draft_table:
        cols = row.find_all('td')
        if cols:
            player_data = {
                'Round': cols[0].text.strip(),
                'Pick': cols[1].text.strip(),
                'Team': cols[2].text.strip(),
                'Player': cols[3].text.strip(),
                'Position': cols[4].text.strip(),
                'Age': cols[5].text.strip(),
                'College/Univ': cols[-1].text.strip() if cols[-1].a else None
            }
            drafted_players.append(player_data)
            print(player_data)  # Debugging line

    return drafted_players

def save_to_csv(players, year):
    if not players:
        print(f"No data found for the year {year}")
        return

    keys = players[0].keys()
    with open(f'nfl_draft_{year}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(players)

year = 2023
players = scrape_nfl_draft(year)
save_to_csv(players, year)
