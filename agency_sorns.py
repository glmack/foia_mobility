from numpy.core.fromnumeric import _diagonal_dispatcher
import requests
import pandas as pd
import re

# [dos, gsa, ded, dod, ]

def get_dos_sorns():
    """Get list of record systems of US Department of State"""
    import requests
    url = 'https://www.state.gov/system-of-records-notices-privacy-office/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('tbody')
    dataset_els = body.find_all('tr')
    datasets = []
    dataset_row = {}
    for dataset_idx, dataset_el in enumerate(dataset_els):
        if dataset_idx == 0:
            pass
        elif dataset_idx != 0:
            column_els = dataset_el.find_all('td')
            for col_idx, col_el in enumerate(column_els):
                if col_idx == 0:
                    # TODO - Lee: split rec_sys_name from recsys_code
                    name_and_code = col_el.text.split()
                    name = name_and_code[0].strip()
                    name_code = name_and_code[1].strip()
                    dataset_row = {'name': name,
                                   'name_code': name_code
                                  }
                elif col_idx == 1:
                    pass
                elif col_idx == 2:
                    dataset_row['sorn_code'] = col_el.text.strip())
                    try:
                        doc_url = col_el.a['href']
                        dataset_row['doc_url'] = doc_url
                    except:
                        pass
                else:
                    pass
            datasets.append(dataset_row)
        else:
            pass
    return datasets


def get_gsa_sorns():
    """Get list of record systems of US General Services Administration"""
    import requests
    url = 'https://www.gsa.gov/reference/gsa-privacy-program/systems-of-records-privacy-act/system-of-records-notices-sorns-privacy-act'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('tbody')
    dataset_els = body.find_all('tr')[0::2]
    datasets = []
    dataset_row = {}
    for dataset_el in dataset_els:
        column_els = dataset_el.find_all('td')
        for column_idx, column_el in enumerate(column_els):
            if column_idx == 0:
                dataset_row = {'dataset_code': column_el.text, 
                               'doc_url': column_el.a['href']
                              }
            elif column_idx == 1:
                dataset_row['title'] = column_el.strong.text
            elif column_idx == 2:
                dataset_row['date_sorn'] = column_el.text
            else:
                pass
        datasets.append(dataset_row)
    return datasets

        



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