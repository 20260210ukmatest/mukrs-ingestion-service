import requests

def download_from_ema(ema_id: int) -> str:
    key = str(ema_id).zfill(2) if ema_id < 100 else str(ema_id)
    url = f'http://mahjong-europe.org/ranking/Tournament/TR_RCR_{key}.html'
    print(f'Downloading URL {url}')
    res = requests.get(url)
    res.raise_for_status()
    return res.text