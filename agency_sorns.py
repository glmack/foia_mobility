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
    datasets = []
    table_row = {}

    body = soup.find('tbody')
    table_row_els = body.find_all('tr')
    for table_row_idx, table_row_el in enumerate(table_row_els):
        if table_row_idx == 0:
            pass
        elif table_row_idx != 0:
            table_data_els = table_row_el.find_all('td')
            for table_data_idx, table_data_el in enumerate(table_data_els):
                if table_data_idx == 0:
                    # TODO - Lee: split rec_sys_name from recsys_code
                    name_and_code = table_data_el.text.split(',')
                    try:
                        name = name_and_code[0].strip()
                    except:
                        name = ''
                    try:
                        name_code = name_and_code[1].strip()
                    except:
                        name_code = ''
                    table_row = {'name': name,
                                   'name_code': name_code
                                      }
                elif col_idx == 1:
                    pass
                elif col_idx == 2:
                    table_row['sorn_code'] = col_el.text.strip()
                    try:
                        doc_url = table_data_string['href']
                        table_row['doc_url'] = doc_url
                    except:
                        pass
                else:
                    pass
            datasets.append(table_row)
        else:
            pass
    return datasets


def get_treasury_sorns():
    """Get list of record systems of US Department of Treasury"""
    url = 'https://home.treasury.gov/footer/privacy-act/system-of-records-notices-sorns'
    import requests
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('section')
    table_els = body.find_all('table')
    datasets = [] # TODO Lee check indent?


    for table_el in table_els:
        dataset_row = {} # TODO Lee check indent
        dataset_els = body.find_all('tr')
        table_el.text

        for dataset_idx, dataset_el in enumerate(dataset_els):
            if dataset_idx == 0:
                pass
            elif dataset_idx != 0:
                table_data_els = dataset_el.find_all('td')
                for table_data_idx, table_data_el in enumerate(table_data_els):
                    table_data_string = table_data_el.a.text.split('-')
                    if table_data_idx == 0:
                        # TODO - Lee: split rec_sys_name from recsys_code
                        try:
                            name_code = table_data_string[0].strip()
                        except:
                            name_code = ''
                            pass
                        dataset_row = {'name_code': name_code
                                      }
                    elif col_idx == 1:
                        try:
                            name = table_data_string[1].strip()
                        except:
                            name = ''
                            pass
                        dataset_row['name'] = name
                    elif col_idx == 2:
                        dataset_row['sorn_code'] = table_data_string[2].strip()
                        try:
                            doc_url = col_el.a['href']
                            dataset_row['doc_url'] = doc_url
                        except:
                            doc_url = ''
                            pass
                    else:
                        pass
                datasets.append(dataset_row)
            else:
                pass
    return datasets


def get_ded_sorns():
    """Get list of record systems of US Department of Education"""
    url = 'https://www2.ed.gov/notices/ed-pia.html'


def get_dod_sorns():
    """Get list of record systems of US Department of Education"""
    url = 'https://dpcld.defense.gov/Privacy/SORNsIndex/'


def get_usda_sorns():
    """Get list of record systems of US Department of Agriculture"""
    url = 'https://www.ocio.usda.gov/policy-directives-records-forms/records-management/system-records'


def get_   _sorns():
    """Get list of ___ record systems from website"""
    url = 'https://www.usa.gov/federal-agencies/u-s-department-of-commerce'

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


# ------------------- non-executive agencies
def get_gsa_sorns():
    """Get list of record systems of US General Services Administration US Commerce"""
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