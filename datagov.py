

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
