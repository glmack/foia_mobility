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
                             order: list = ['Relevance']
                             ) -> dict:
    """Search documents in Federal Register via API GET request"""
   
    params = {'fields[]': [
        'abstract', 'action', 'agencies', 'agency_names', 'body_html_url', 
        'citation', 'document_number', 'effective_on', 'end_page',
        'html_url','publication_date', 'start_page', 'title', 'subtype',
        'toc_doc', 'toc_subject', 'topics', 'type', 'volume'
        ],
        'conditions[term]': search_terms,
        'conditions[type]': doc_type
              # 'conditions[agencies][]': agencies,
              # 'conditions[publication_date][gte]': pub_start_date,
              # 'conditions[publication_date][lte]': pub_end_date,
              # 'conditions[effective_date][is]': exact_date,
              # 'conditions[topics][]': topic_tags
              }
    response = requests.get('https://federalregister.gov/api/v1/documents.json', params)
    # https://www.federalregister.gov/api/v1/documents.json?fields%5B%5D=abstract&per_page=20&order=relevance&conditions%5Bterm%5D=concur&conditions%5Btype%5D%5B%5D=NOTICE
    data = response.json()
    results = data['results']

    # TODO
    

    while data['next_page_url']:
        response = requests.get(data['next_page_url'])
        data = response.json()
        results_pg = data['results']
        results.append(results)
    # 'next_page_url': 'https://www.federalregister.gov/api/v1/documents?conditions%5Bterm%5D=travel&conditions%5Btype%5D=NOTICE&fields%5B%5D=abstract&fields%5B%5D=action&fields%5B%5D=agencies&fields%5B%5D=agency_names&fields%5B%5D=body_html_url&fields%5B%5D=citation&fields%5B%5D=document_number&fields%5B%5D=effective_on&fields%5B%5D=end_page&fields%5B%5D=excerpts&fields%5B%5D=executive_order_notes&fields%5B%5D=html_url&fields%5B%5D=publication_date&fields%5B%5D=start_page&fields%5B%5D=title&fields%5B%5D=toc_doc&fields%5B%5D=toc_subject&fields%5B%5D=topics&fields%5B%5D=type&fields%5B%5D=volume&format=json&page=2'

    return results

def filter_fedregister_travel_sorns(response_dict):
    


def scan_travel_sorns():
    """Get system of records notices (SORNs) for travel datasets in usgov agencies"""
    pass


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
