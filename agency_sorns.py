from numpy.core.fromnumeric import _diagonal_dispatcher
import requests
import pandas as pd
import re

# [dos, gsa, ded, dod, ]

def get_dos_sorns():
    """Get list of Department of State record systems from website"""
    import requests
    url = 'https://www.state.gov/system-of-records-notices-privacy-office/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('tbody')
    dataset_els = body.find_all('tr')
    datasets = []
    dataset_row = {}
    for dataset_idx, dataset_el in enumerate(dataset_els):
        print(f'dataset_idx: {dataset_idx}')
        if dataset_idx == 0:
            pass
        elif dataset_idx != 0:
            column_els = dataset_el.find_all('td')
            for col_idx, col_el in enumerate(column_els):
                print(f'col_idx: {col_idx}')
                if col_idx == 0:
                    dataset_row = {'name': col_el.text}
                    print(f'col_el text: {col_el.text}')
                elif col_idx == 1:
                    pass
                elif col_idx == 2:
                    dataset_row['sorn_code'] = col_el.text.strip()
                    print(f'col_el text: {col_el.text.strip()}')
                    try:
                        doc_url = col_el.a['href']
                        dataset_row['doc_url'] = col_el.a['href']
                        print(f'col_el url: {doc_url}')
                    except:
                        pass
                else:
                    pass
            datasets.append(dataset_row)
        else:
            pass
    return datasets


def get_gsa_sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 'https://www.gsa.gov/reference/gsa-privacy-program/systems-of-records-privacy-act/system-of-records-notices-sorns-privacy-act'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('tbody')
    dataset_els = body.find_all('tr')
    datasets = []
    dataset_row = {}


def get_ded_sorns():
    """Get list of Department of Education record systems from website"""


def get_dod_sorns():
    """Get list of Department of Education record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""


def get_   _sorns():
    """Get list of ___ record systems from website"""