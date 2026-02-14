import re

def __regex_replace(text, search_regex, replace_text):
    p = re.compile(search_regex)
    return p.sub(replace_text, text)

def clean_ema_data(ema_id, text):
    match ema_id:
        case 52:
            __regex_replace(text, "17-mars-13", "17 Mar 2013")
        case 94:
            __regex_replace(text, "31 Jan\\. 1 Feb 2015", "31 Jan 2015")
        case 224:
            __regex_replace(text, "23-24 Mars 2019", "23 Mar 2019")
        case 227 | 228:
            __regex_replace(text, "13-14 Apr\\.2019", "13 Apr 2019")
        case 242:
            __regex_replace(text, "20.21 Jul\\. 2019", "20 Jul 2019")
        case 265:        
            __regex_replace(text, "18 Janv\\. 2020", "18 Jan 2020")
        case 306:
            __regex_replace(text, "16 - 17 SEP 2023","16 Sep 2023")
    return text