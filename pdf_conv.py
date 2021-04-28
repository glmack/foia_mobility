# import tabula
import requests
# import matplotlib.pyplot as plt
# import pandas as pd


def get_datagov_orgs():
    """Get org codes for organizations with datasets on data.gov"""
    import requests
    import os
    params = {'api_key': os.environ['DATAGOV_API_KEY']}
    response = requests.get('https://api.gsa.gov/technology/datagov/v3/action/organization_list',
                            params)
    data = response.json()
    return data


def filter_datagov_fed_orgs(datagov_orgs):
    """Filter data.gov api org code list for codes of US federal agencies and departments"""
    filter_string = 'gov'
    drops = ['cdph-ca-gov',
             'cdatribe-nsn-gov',
             'nsgic-local-govt-gis-inventory',
             'louisville-metro-government',
             'arkansas-gov',
             'ca-gov',
             'nc-gov',
             'nd-gov',
             'louisville-metro-government']
    fed_orgs = [org for org in datagov_orgs['result'] if filter_string in org]
    fed_orgs = [org for org in fed_orgs if org not in drops]
    return fed_orgs


def get_datagov_meta(search_term):
    """Query data.gov for metadata on us gov data sets"""
    import requests
    import os
    params = {'q': search_term,
              'api_key': os.environ['DATAGOV_API_KEY']}
    response = requests.get(
        'https://api.gsa.gov/technology/datagov/v3/action/package_search',
        params=params
        )
    data = response.json()
    return data


def filter_datagov_meta_by_org(payload):
    """Filter datagov api response by US federal government orgs"""
    usgov_orgs = filter_feds_datagov_orgs(orgs)
    data = [i for i in payload['result']['results'] if i['organization']['name'] in usgov_orgs]
    return data
    

def datagov_to_pd():
    """Read datagov api query responses into pandas and pre-process"""
    pass
    # data['result']['results'][0]


def get_datagov_resource():
    """Request resources from datagov api"""
    import os
    import requests
    params = {'q': 'concur',
              'api_key': os.environ['DATAGOV_API_KEY']}
    response = requests.get(response = requests.get(
        'https://api.gsa.gov/technology/datagov/v3/action/resource_search',
        params=params
        ))
    data = response.json()
    return data


def get_concur_travel_parent_meta():
    """Request metadata on US gov datasets from data.gov"""
    import requests
    params = {'id': 'concur-travel-parent',
               'api_key': os.environ['DATAGOV_API_KEY']}
    response = requests.get(
        'https://api.gsa.gov/technology/datagov/v3/action/package_show',
        params=params
        )
    data = response.json()
    return data

# Document Status               https://catalog.data.gov/dataset/document-status
# E2                            https://catalog.data.gov/dataset/e2
# Group Update                  https://catalog.data.gov/dataset/group-update
# User Profile                  https://catalog.data.gov/dataset/user-profile
# E-Gov Travel (ETS) Measures   https://catalog.data.gov/dataset/e-gov-travel-ets-measures
# Master Data                   https://catalog.data.gov/dataset/master-data-b4599
# End to End Travel             https://catalog.data.gov/dataset/end-to-end-travel
# Travel Manager - Production   https://catalog.data.gov/dataset/travel-manager-production


def get_fedreg_usg_agencies():
    """Get list of usgov agencies from federalregister.gov api"""
    import requests
    import os
    response = requests.get('https://federalregister.gov/api/v1/agencies')
    data = response.json()
    return data


def search_fedreg_docs(search_terms: list = None,
                       doc_type: str = None,
                       per_page: int = 100,
                       page: int = 1,
                       year: str = None,
                       order: list = ['Relevance'],
                       pub_start_date: str = None, #YYYY-MM-DD
                       pub_end_date: str = None, #YYYY-MM-DD
                       effective_start_date: str = None, # YYYY-MM-DD
                       effective_end_date: str = None, #YYYY-MM-DD
                       effective_exact_date: str = None, #YYYY-MM-DD
                       # effective_year: str = None, #YYYY
                       # topic_tags: list[str] = None,
                       agencies: list = None
                      ) -> dict:
    """Search documents in Federal Register via API GET request"""
 
    total_results = []

    params = {'fields[]': [
        'abstract', 'action', 'agencies', 'agency_names', 'body_html_url', 
        'citation', 'document_number', 'effective_on', 'end_page',
        'html_url','publication_date', 'start_page', 'title', 'subtype',
        'toc_doc', 'toc_subject', 'topics', 'type', 'volume'
        ],
        'conditions[term]': search_terms,
        'conditions[type]': doc_type,
        'per_page': per_page,
        'conditions[effective_date][year]': year,
        'conditions[agencies][]': agencies,
        'conditions[publication_date][gte]': pub_start_date,
        'conditions[publication_date][lte]': pub_end_date,
        'conditions[effective_date][gte]': effective_start_date,
        'conditions[effective_date][lte]': effective_end_date,
        'conditions[effective_date][is]': effective_exact_date,
        # 'conditions[effective_date][year]': effective_year,
        # 'conditions[topics][]': topic_tags
              }

    has_next_page = False
    next_page = ""

    # endpoint: GET​/documents.{format}
    response = requests.get('https://federalregister.gov/api/v1/documents.json', params)
    data = response.json()
    results = data['results']
    len_results = len(results)
    total_pages = data['total_pages']
    count = data['count']
    
    if 'next_page_url' in data:
        has_next_page = True

    while 'next_page_url' in data:
        total_results.extend(results)
        next_page_2 = data['next_page_url']
        
        # call next page
        response = requests.get(next_page_2)
        data = response.json()
    
    results = data['results']
    total_results.extend(results)

    return total_results


def get_unique_actions(notices):
    """Return list of notice 'action' tags from usgov federal register api response"""
    action_tags = []
    # [action_tags.append(i['action'].lower()) for i in notices if i['action'] is not None]
    for i in notices:
        if i['action'] is not None:
            action_tags.append(i['action'].lower())
        else:
            continue
    action_tags = set(action_tags)
    a_tags = list(action_tags)
    a_tags.sort()
    # a_tags_filtered = [i for i in a_tags] # if any(j in i for j in ['record', 'system'])]
    return a_tags


def filter_sorns(notices):
    """Filter notice results for system of record notices""" 
    matches = ['system', 'record']
    action_match_notices = []
    abstract_match_notices = []
    no_match_notices = []
    other_notices = []
    none_notices = []
    other_notices = []
    for i in notices:

        if i['action'] is None and i['abstract'] is None:
            none_notices.append(i)
        
        elif i['action'] is not None and i['abstract'] is not None:
            if any(match in i['action'].lower() for match in matches):
                action_match_notices.append(i)
            elif all(match in i['abstract'].lower() for match in matches):
                abstract_match_notices.append(i)
            else:
                no_match_notices.append(i)

        elif i['action'] is not None and i['abstract'].lower() is None:
            if any(match in i['action'].lower() for match in matches):
                abstract_match_notices.append(i)
            else:
                no_match_notices.append(i)

        elif i['action'] is None and i['abstract'].lower() is not None:
            if all(match in i['abstract'].lower() for match in matches):
                abstract_match_notices.append(i)
            else:
                no_match_notices.append(i)
        
        else:
            other_notices.append(i)
    
    return action_match_notices, abstract_match_notices, no_match_notices, none_notices, other_notices
            

def filter_sorn_operations(notices):
    """Categorize federal register api response based on update type"""
    created_notices = []
    modified_notices = []
    deleted_notices = []
    other_notices = []
    blank_notices = []

    # TODO (Lee) - account for keywords 'system', 'systems', and 'records'

    # TODO (Lee) - account for blank and generic 'Notice' actions, ('systems of records' - plural ?)e.g.:
    # 'body_html_url': 'https://www.federalregister.gov/documents/full_text/html/2010/06/07/2010-13481.html',
    # 'https://www.federalregister.gov/documents/full_text/html/2010/07/26/2010-17934.html',
    # 'body_html_url': 'https://www.federalregister.gov/documents/full_text/html/2011/01/05/2010-33295.html',

    # TODO (Lee) - keywords: ['new', 'add', 'establish', 'proposed', 'reinstate']
    created_indicators = [
        'notice of a new system of records.', 
        'notice to add a system of records.'
        'notice of privacy act system of records.',
        'notice to establish systems of records.',
        'notice of a new privacy act system of records.',
        'notice of a new system of records.',
        'notice of a new system of records; and rescindment of four system of records notices.',
        'notice of new privacy act system of records.',
        'notice of privacy act system of records.',
        'notice of proposed privacy act system of records.',
        'notice of proposed new system of records.',
        'notice to add a system of records.',
        'notice to establish systems of records.',
        'notice to reinstate a system of records.']

    # TODO (Lee): keywords = ['modified', 'amend', 'alter', 'altered', 'amendment', 'modification', 'revised']
    modified_indicators = [
        'notice of a modified system of records.',
        'notice to amend a system of records.',
        'notice of modification to existing Privacy Act system of records.',
        'notice of amendment of Privacy Act system of records.',
        'notice to alter a system of records.',
        'altered system of records and housekeeping changes.',
        'notice of a modified privacy act system of records.',
        'notice of a modified system of records.',
        'notice of amendment of privacy act system of records.',
        'notice of amendment to system of records.',
        'notice of changes to systems of records and addition of routine use.',
        'notice of general amendment to federal reserve board of governors systems of records.',
        'notice of modification to existing privacy act system of records.',
        'notice of modified privacy act system of records.',
        'notice of modified system of records.',
        'notice of modified systems of records.',
        'notice to alter a system of records.',
        'notice to alter an existing privacy act system of records.',
        'notice to amend a system of records.',
        'notice of revised privacy act system notices.', # does not contain word 'record'
        'notice of revised systems of records.',
        'notice to amend a record system.'
    ]

    # TODO (Lee): keywords = ['rescind', 'delete', 'rescindment']
    deleted_indicators = [
        'rescindment of a system of records.',
        'notice to delete a system of records.',
        'rescindment of a system of records notice (sorn).',
        'rescindment of a system of records notice.',
        'rescindment of notices and notice of a new system of records.',
        'notice to delete a system of records.'
    ]

 # others/multiple actions:'notice of the rescission, establishment, and amendment of systems of records.',,
 # 'notice to reinstate a system of records.',
 # 'notice: publication of new and revised systems of records and standard disclosures.',

    for i in notices:
        if i['action'] is None:
            blank_notices.append('')
        elif i['action'].lower() in created_indicators:
                created_notices.append(i)
        elif i['action'].lower() in modified_indicators:
            modified_notices.append(i)
        elif i['action'].lower() in deleted_indicators:
            deleted_notices.append(i)
        else:
            other_notices.append(i)
    return created_notices, modified_notices, deleted_notices, other_notices, blank_notices


def get_record_system_names(notices):
    """Extract fields from sorn doc html"""
    import requests
    from bs4 import BeautifulSoup
    system_names = []
    for notice in notices:
        print('notice')
        url = notice['body_html_url']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        name_header = soup.find(text=re.compile('SYSTEM NAME AND NUMBER'))
        # h3_tag = soup.h3 #(string ='SYSTEM NAME AND NUMBER')
        # TODO (Lee) include h2_tag also

        # (text=lambda t: t and any(x in t for x in ['Open', 'Closed']))
        if name_header is not None:
            name_data = name_header.findNext('p').text
            if name_data is not None:
                print('dp is not none')
                notice['system_name'] = name_data
            else:
                print('else 1')
                continue
        elif name_header is None:
            print('else 2: sytem name is none')
        else:
            print('others')
            continue
    return notices


def get_d2d_trip_report():
    """Get 2/2020 trip report from d2d dashboard"""
    filepath = '/Users/lee/Documents/code/foia_mobility/TRip_Relocation.pdf'
    response = requests.get('https://d2d.gsa.gov/report/gsa-ogp-business-travel-and-relocation-dashboard')
    dfs = tabula.read_pdf(filepath, multiple_tables=True, pages=8)
    df_total_2019 = dfs[1]
    return df_total_2019


def vis_trip_report():
    """Visualize trip report data"""
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=total_2019.values, colLabels=total_2019.columns, loc='center')
    fig.tight_layout()
    plt.show()


def get_foiaonline_travel():
    import requests
    payload = {'query': 'travel'}
    response = requests.get('https://foiaonline.gov/foiaonline/action/public/search/quickSearch')
    data = response.json()
    return data


def get_foia_library_list():
    """Get list of foia libraries from DeLuca journal article"""
    import requests
    response = requests.get('https://works.bepress.com/lisa_deluca/40/download/')
    pd.read_excel()


def get_travel_govinfogov():
    pass


def get_stakeholders():
    pass


def get_regulation():
    """Make call to us gov gsa regulations api"""
    payload = {'filter[searchTerm]': '115–34',
               'api_key': os.environ['DATAGOV_API_KEY']}
    response = requests.get(
        'https://api.regulations.gov/v4/documents?3&api_key=DEMO_KEY',
        params=payload
        )
    data = response.json()
    return data


# ----------

concur_travel_parent_meta = get_concur_travel_parent_meta()

docs = search_fedreg_docs(search_terms='system of records+travel', 
                          doc_type='NOTICE', 
                          per_page=100, 
                          effective_start_date='1994-01-01',
                          effective_end_date='2020-12-31')')

sfr1 = search_fedreg_docs(search_terms='system of records+travel',
                          doc_type='NOTICE',
                          per_page=100,
                          effective_start_date='2010-01-01',
                          effective_end_date='2020-12-31')

fs1 = filter_sorns(sfr1)


# actions_set = get_unique_actions(notices)


# ----------
# TODO (Lee) - evaluate agency sites that describe sorns, e.g.:
# https://home.treasury.gov/footer/privacy-act/system-of-records-notices-sorns
# https://www.dhs.gov/system-records-notices-sorns
