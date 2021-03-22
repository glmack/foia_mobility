import tabula
import requests
import matplotlib.pyplot as plt
import pandas as pd


def get_datagov_orgs():
    """Get org codes for organizations with datasets on data.gov"""
    import requests
    import os
    params = {'api_key': os.environ['DATAGOV_API_KEY']}
    response = requests.get('https://api.gsa.gov/technology/datagov/v3/action/organization_list',
                            params)
    data = response.json()
    return data


def filter_feds_datagov_orgs(datagov_orgs):
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

# https://home.treasury.gov/footer/privacy-act/system-of-records-notices-sorns
# https://www.dhs.gov/system-records-notices-sorns


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


def get_usgov_agencies():
    """Get list of usgov agencies from federalregister.gov api"""
    import requests
    import os
    response = requests.get('https://federalregister.gov/api/v1/agencies')
    data = response.json()
    return data


def search_fed_reg_docs(search_terms: list = None,
                        doc_type: str = None,
                        per_page: int = 100,
                        page: int = 1,
                        year: str = None,
                        order: list = ['Relevance'],
                        pub_start_date: str = None, #YYYY-MM-DD
                        pub_end_date: str = None, #YYYY-MM-DD
                        effective_start_date: str = None, # YYYY-MM-DD
                        effective_end_date: str = None, #YYYY-MM-DD
                        agencies: list = None
                        ) -> dict:
    """Search documents in Federal Register via API GET request"""
   
    # initialize empty list to store results
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
        # 'conditions[effective_date][is]': effective_date,
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


def get_sorn_action_tags(response_d):
    """Return tags for notice 'actions' in USGOV Federal Register api response"""
    action_tags = []
    [action_tags.append(i['action'].lower()) for i in response_d if i['action'] is not None]
    action_tags = set(action_tags)
    a_tags = list(action_tags)
    a_tags.sort()
    [i for i in a_tags if any(j in i for j in ['record', 'system'])]
    return a_tags


def filter_fedreg_notice_results(response_dict):
    """Filter results of federal register api call based on action type"""
    created_notices = []
    modified_notices = []
    deleted_notices = []
    other_notices = []
    blank_notices = []

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
        'notice to add a system of records.',
        'notice to establish systems of records.',
        'notice to reinstate a system of records.']

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
        'notice of revised privacy act system notices.',
        'notice of revised systems of records.'
        'rescindment of a system of records notice (sorn).',
        'rescindment of a system of records notice.',
        'rescindment of notices and notice of a new system of records.'
    ]

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

    # TODO incorporate action_tags into checks below
    for i in response_dict:
        if i['action'] is None:
            blank_notices.append('')
        elif i['action'].lower() in created_indicators:
        # elif i['action'].lower() == 'notice of a new system of records.':
            # 'Notice to add a system of records.'
            # ??? 'Notice of Privacy Act system of records.'
            # 'Notice to establish systems of records.'
                created_notices.append(i)
        elif i['action'].lower() in modified_indicators:
        # elif i['action'].lower() == 'notice of a modified system of records.':
            # 'Notice to amend a system of records.'
            # 'Notice of modification to existing Privacy Act system of records.'
            # 'Notice of amendment of Privacy Act system of records.'
            # 'Notice to alter a system of records.'
            modified_notices.append(i)
        elif i['action'].lower() in deleted_indicators:
            # 'Notice to delete a system of records.'
            deleted_notices.append(i)
        else:
            other_notices.append(i)
    return created_notices, modified_notices, deleted_notices, other_notices, blank_notices


def get_trip_report():
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


# DOL-wide FOIA reading room
# https://www.dol.gov/general/foia/readroom


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
