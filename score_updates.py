from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


url_euro = 'https://www.futbol24.com/international/UEFA/Euro-Championship/2024/'
URL_COPA_AMERICA = 'https://www.futbol24.com/international/CONMEBOL/Copa-America/2024/'


def parse_match(c):
    match = c.a.get('href')
    # regex = r"/([^/]+)/vs/([^/]+)/"
    # matches = re.findall(regex, match)
    matches = None
    if not matches:
        visit_team = c.next.next.next.next.next.next
        local_team = c.previous.previous
    else:
        local_team, visit_team = matches[0]
    score = c.a.text


    return {local_team: score.split('-')[0], visit_team: score.split('-')[1]}

def get_latest_scores(
        url:str = URL_COPA_AMERICA,
        simulate: bool = False
        ):
    if simulate:
        print('Simulating results')
        return [
            {'Argentina': 2, 'Canada': 0},
            {'Peru': 0, 'Chile': 1}
        ]
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table')
    results = []
    for t in tables:
        rows = t.find_all('tr')
        for r in rows:
            cols = r.find_all('td')
            for c in cols:
                if 'dash' in c.get_attribute_list('class'):
                    try:
                        #print(c.a.get('href'))
                        #print(c)
                        # import pdb; pdb.set_trace()
                        results.append(parse_match(c))
                    except Exception:
                        pass
    return results


