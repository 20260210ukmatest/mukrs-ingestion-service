from dateutil import parser

from services.get_country_from_img_link import get_country_from_img_link

def __parse_tournament_info_cell(cell):
    return cell.find_all('td')[1].get_text(strip=True).replace('\n', '')

def __parse_tournament_info_date(cell):
    date = __parse_tournament_info_cell(cell)
    if '-' in date:
        cleaned_date = date.split(' ')[0].split('-')[0] + ' ' + date.split(' ')[
            1].replace('.', '') + ' ' + date.split(' ')[2]
        return parser.parse(cleaned_date)
    else:
        return parser.parse(date)

def parse_tournament_info(soup):
    table = soup.find('table')
    rows = table.find_all('tr')

    mers_weight_text = __parse_tournament_info_cell(rows[6]).replace(',','.')
    index_of_open_bracket = mers_weight_text.find('(')
    days = int(mers_weight_text[index_of_open_bracket + 6])
    weight = float(mers_weight_text[:index_of_open_bracket])

    return {
        'ema_id': __parse_tournament_info_cell(rows[1]),
        'name': __parse_tournament_info_cell(rows[2]),
        'place': __parse_tournament_info_cell(rows[3]).replace('(see National Stats)',''),
        'country': get_country_from_img_link(rows[3].find_all('td')[1]),
        'date': __parse_tournament_info_date(rows[4]),
        'players': __parse_tournament_info_cell(rows[5]),
        'mers_weight': weight,
        'mukrs_days': days
    }