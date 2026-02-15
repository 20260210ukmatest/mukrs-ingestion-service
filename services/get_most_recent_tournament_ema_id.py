import bs4
import requests

from datetime import datetime

def get_most_recent_tournament_ema_id():
    current_year = datetime.now().year
    url = f'http://mahjong-europe.org/ranking/Tournament/Tournaments_{current_year}.html'
    print(f'Downloading URL {url}')
    res = requests.get(url)
    if (res.status_code == 404):
        url = f'http://mahjong-europe.org/ranking/Tournament/Tournaments_{current_year-1}.html'
        print(f'URL not found, downloading URL {url}')
        res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    riichi_tournaments_table = soup.select('div.TCTT_lignes')[1]
    most_recent_tournament_row = riichi_tournaments_table.select('div')[-1]
    most_recent_tournament_ema_id_str = most_recent_tournament_row.select('p')[0].get_text(strip=True)
    return int(most_recent_tournament_ema_id_str)
