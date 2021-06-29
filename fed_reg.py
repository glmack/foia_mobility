import requests
import pandas as pd
import re


def get_usg_agencies():
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
    """Search documents in Federal Register via API"""
 
    total_results = []

    params = {'fields[]': [
        'abstract', 'action', 'agencies', 'agency_names', 'body_html_url', 
        'citation', 'document_number', 'effective_on', 'end_page',
        'html_url','publication_date', 'start_page', 'title',
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

    total_results.extend(data['results'])

    while 'next_page_url' in data:
        response = requests.get(data['next_page_url'])
        data = response.json()
        total_results.extend(data['results'])

    return total_results


def filter_sorns(notices):
    """Filter notice results for system of record notices""" 
    action_keywords = ['system', 'record']
    title_keywords = ['system', 'record', 'privacy']
    abstract_keywords = ['system', 'record', 'privacy']
    action_matches = []
    abstract_matches = []
    title_matches = []
    no_matches = []
    other_notices = []
    none_notices = []

    for notice in notices:
        if notice['action'] is None and notice['abstract'] is None and notice['title'] is None:
            none_notices.append(notice)
        
        elif notice['action'] is not None or notice['abstract'] is not None or notice['title'] is not None:
            action = xstr(notice['action']).lower()
            abstract = xstr(notice['abstract']).lower()
            title = xstr(notice['title']).lower()
            # fields = [action, abstract, notice]
            
            if all(x in action for x in action_keywords):
                action_matches.append(notice)
            elif all(x in abstract for x in abstract_keywords):
                abstract_matches.append(notice)
            elif all(x in title for x in title_keywords):
                title_matches.append(notice)
            else:
                no_matches.append(notice)
        
        else:
            pass
    
    return action_matches, abstract_matches, title_matches, no_matches, none_notices, other_notices


def xstr(s):
    if s is None:
        return ''
    return str(s).lower()


def get_unique_actions(notices):
    """Return list of notice 'action' tags from us federal register api"""
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


def get_rec_sys_names(notices):
    """Extract record system name and number fields from sorn full text"""
    import requests
    from bs4 import BeautifulSoup
    
    system_names = []
    notices_named = []
    notices_namenulls = []
    
    for notice in notices:
        url = notice['body_html_url']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        name_paragraph = soup.find(text=re.compile('system name', re.IGNORECASE))

        if name_paragraph is not None:
            name_data = name_paragraph.findNext('p').text
            if name_data is not None:
                notice['system_name_num'] = name_data
                notices_named.append(notice)
            else:
                notices_namenulls.append(name_data)
                continue
        else:
            notices_namenulls.append(notice)
            continue

    return notices_named, notices_namenulls

            
# TODO (Lee) improve this through keyword-based approach
def classify_sorn_operations(notices):
    """Categorize federal register api response based on update type"""
    created_notices = []
    modified_notices = []
    deleted_notices = []
    other_notices = []
    blank_notices = []

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

 # others/multiple actions: 'notice of the rescission, establishment, and amendment of systems of records.',,
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


def classify_sorns_fulltext(notices):
    """Classifies travel-related sorns through full text search"""
    import requests
    from bs4 import BeautifulSoup
    travel_sorns = []
    nontravel_sorns = []

    for notice in notices:
        url = notice['body_html_url']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        travel_keywords = soup.find(text = re.compile('travel', re.IGNORECASE))

        if travel_keywords is not None:
            travel_sorns.append(notice)
        
        elif travel_keywords is None:
            nontravel_sorns.append(notice)

        else:
            continue
    
    return travel_sorns, nontravel_sorns


# ----------

docs1 = search_fedreg_docs(search_terms='record+system', 
                          doc_type='NOTICE', 
                          per_page=100, 
                          effective_start_date='1994-01-01',
                          effective_end_date='1999-12-31')

docs2 = search_fedreg_docs(search_terms='record+system', 
                          doc_type='NOTICE', 
                          per_page=100, 
                          effective_start_date='2000-01-01',
                          effective_end_date='2009-12-31')

docs3 = search_fedreg_docs(search_terms='record+system', 
                          doc_type='NOTICE', 
                          per_page=100, 
                          effective_start_date='2010-01-01',
                          effective_end_date='2021-12-31')

docs = docs1 + docs2 + docs3
filtered_docs = filter_sorns(docs)
filtered_matches = filtered_docs[1] + filtered_docs[2] + filtered_docs[3]
matchdf = pd.DataFrame(filtered_matches)
matchdf = matchdf.drop('subtype', axis=1)

travel_docs = search_fedreg_docs(search_terms='record+system+travel',
                                 doc_type='NOTICE',
                                 per_page=100,
                                 effective_start_date='1994-01-01',
                                 effective_end_date='2020-12-31')

filtered_travel_docs = filter_sorns(travel_docs)

travel2_sorns = search_notices_for_travel(fs0[0])

# uncomment to run
# actions_set = get_unique_actions(notices)