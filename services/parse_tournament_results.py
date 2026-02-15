import uuid

from services.get_country_from_img_link import get_country_from_img_link
from models.player import PlayerModel
from bs4 import BeautifulSoup

def parse_tournament_results(soup: BeautifulSoup) -> dict[PlayerModel, int]:
    score_divs = soup.select('.TCTT_lignes')[0].select('div')
    data = {}
    # skip the headers at index 0
    for row in score_divs[1:]:
        row_ps = row.select('p')
        # row_ps[0] is position
        last_name = row_ps[2].get_text(strip=True).casefold()
        first_name = row_ps[3].get_text(strip=True).casefold()
        if first_name == "-" and last_name == "-":
            last_name = str(uuid.uuid4())
        # remove empty values
        ema_number = row_ps[1].get_text(strip=True)
        if ema_number == "-":
            ema_number = None
        base_rank_text = row_ps[7].get_text(strip=True)
        if base_rank_text == "-" or base_rank_text == "N/A":
            continue
        player = PlayerModel(first_name=first_name, last_name=last_name, country=get_country_from_img_link(row_ps[4]) or '??', ema_number=ema_number)
        data[player] = int(base_rank_text)
    return data