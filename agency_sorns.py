from numpy.core.fromnumeric import _diagonal_dispatcher
import requests
import pandas as pd
import re

# TODO Lee refactor/abstract to class structure [dos, gsa, ded, dod, ]
# TODO Lee - add 'org_scope' field with name of agency/sub-agency 

def get_dos_sorns():
    """Get list of record systems of US Department of State"""
    import requests
    url = 'https://www.state.gov/system-of-records-notices-privacy-office/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}

    body = soup.find('tbody')
    tr_els = body.find_all('tr')
    for tr_idx, tr_el in enumerate(tr_els):
        if tr_idx == 0: # header row of table
            pass
        else:
            td_els = tr_el.find_all('td')
            for td_idx, td_el in enumerate(td_els):
                if td_idx == 0:
                    # TODO - Lee: split rec_sys_name from recsys_code
                    data = td_el.text.split(',')
                    try:
                        name = data[0].strip()
                    except:
                        name = ''
                    try:
                        name_code = data[1].strip()
                    except:
                        name_code = ''
                    rec_sys = {'name': name,
                                   'name_code': name_code
                                      }
                elif td_idx == 1:
                    pass

                elif td_idx == 2:
                    rec_sys['sorn_code'] = td_el.text.strip()
                    # TODO Lee - not getting url correctly
                    try:
                        doc_url = td_el.a['href']
                        rec_sys['doc_url'] = doc_url
                    except:
                        pass
                else:
                    pass
            rec_systems.append(rec_sys)
    return rec_systems


def get_treasury_sorns():
    """Get list of record systems of US Department of Treasury"""
    url = 'https://home.treasury.gov/footer/privacy-act/system-of-records-notices-sorns'
    import requests
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('section')
    table_els = body.find_all('table')
    rec_systems = []
    rec_sys = {}

    for table in table_els:
        tr_els = body.find_all('tr')
        for tr_idx, tr_el in enumerate(tr_els):
            if tr_idx == 0:
                pass
            else:
                td_els = tr_el.find_all('td')
                for td_idx, td_el in enumerate(td_els):
                    if td_idx == 0:
                        try:
                            data = td_el.a.text.split('-')
                        except:
                            data = ''
                            pass
                        try:
                            doc_url = td_el.a['href']
                        except:
                            doc_url = ''
                            pass
                        try:
                            name_code = data[0].strip()
                        except:
                            name_code = ''
                            pass
                        try:
                            name = data[1].strip()
                        except:
                            name = ''
                            pass
                        try:
                            sorn_code = data[2].strip()
                        except:
                            sorn_code = ''
                            pass
                        rec_sys = {'name': name,
                                'name_code': name_code,
                                'sorn_code': sorn_code,
                                'doc_url': doc_url}
                    elif td_idx == 1:
                        pass
                    elif td_idx == 2:
                        pass
                    else:
                        pass
                rec_systems.append(rec_sys)
    return rec_systems


def get_commerce_sorns():
    """Get list of record systems of US Department of Commerce"""
    import requests
    url = 'https://www.osec.doc.gov/opog/privacyact/PrivacyAct_SORNs.html#Department'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}

    accordions = soup.find_all('div', class_ ='AccordionPanelContent')
    for accordion in accordions:
        try:
            name = accordion.ul.li.text
        except:
            name = ''
            pass
        try:
            doc_url = accordion.ul.li.a['href']
        except:
            doc_url = ''
            pass
        try:
            name_code = accordion.ul.li.a['title']
        except:
            name_code = ''
        rec_sys = {'name': name,
                   'url': doc_url,
                   'name_code': name_code}
        rec_systems.append(rec_sys)

    # tr_els = body.find_all('tr')
    # for tr_idx, tr_el in enumerate(tr_els):
        # if tr_idx == 0: # header row of table
        #     pass
        # else:
        #     td_els = tr_el.find_all('td')
    

        # for td_idx, td_el in enumerate(td_els):
        #     if td_idx == 0:
        #         # TODO - Lee: split rec_sys_name from recsys_code
        #         data = td_el.text.split(',')
        #         try:
        #             name = data[0].strip()
        #         except:
        #             name = ''
        #         try:
        #             name_code = data[1].strip()
        #         except:
        #             name_code = ''
        #         rec_sys = {'name': name,
        #                         'name_code': name_code
        #                             }
        #     elif td_idx == 1:
        #         pass

        #         elif td_idx == 2:
        #             rec_sys['sorn_code'] = td_el.text.strip()
        #             # TODO Lee - not getting url correctly
        #             try:
        #                 doc_url = td_el.a['href']
        #                 rec_sys['doc_url'] = doc_url
        #             except:
        #                 pass
        #         else:
        #             pass
        #     rec_systems.append(rec_sys)
    return rec_systems


def get_ded_sorns():
    """Get list of record systems of US Department of Education"""
    import requests
    url = 'https://www2.ed.gov/notices/ed-pia.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}


def get_dod_sorns():
    """Get list of record systems of US Department of Education"""
    url = 'https://dpcld.defense.gov/Privacy/SORNsIndex/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}

def get_usda_sorns():
    """Get list of record systems of US Department of Agriculture"""
    url = 'https://www.ocio.usda.gov/policy-directives-records-forms/records-management/system-records'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}

def get_   _sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}


def get_   _sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}


def get_   _sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}


def get_   _sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}


def get_   _sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}


def get_   _sorns():
    """Get list of ___ record systems from website"""
    import requests
    url = 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_systems = []
    rec_sys = {}

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