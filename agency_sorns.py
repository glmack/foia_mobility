import requests
import pandas as pd
import re

def get_state_sorns():
    """Scrape list of record systems from Department of State website"""
    import requests
    url = 'https://www.state.gov/system-of-records-notices-privacy-office/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('tbody')
    dataset_els = body.find_all('tr')
    datasets = []
    dataset_row = {}
    for da
    for dataset_idx, dataset_el in enumerate(dataset_els):
        if idx == 0:
            continue
        elif idx != 0:
            columns = dataset_el.find_all('td')
            column_count = 0
            for col_idx, col_el in enumerate(columns):
                if col_idx == 0:
                    dataset_row: {['name'] = col.text}
                    print(column.text)
                elif col_idx == 1:
                    continue
                elif col_idx == 2:
                    dataset_row['sorn_code'] = column.text}
                    print(column.text)
                    dataset_row['sorn_url'] = column.href
                else:
                    continue
        else:
            continue
                datasets.append(dataset_row)
    return datasets
