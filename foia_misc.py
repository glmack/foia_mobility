def get_govwide_sorns():
    """Retrieve US government-wide system of records notices from fpc.gov"""
    import requests
    from bs4 import BeautifulSoup
    response = requests.get('https://www.fpc.gov/resources/SORNs/#container')
    soup = BeautifulSoup(response.content, 'html.parser')
    agency_tags = soup.find_all('div', class_ = 'tabcontent')
    titles = []
    pub_date_docs = []
    for agency in agency_tags:
        try:
            dataset_tags = agency.find_all('button')
            for dataset in dataset_tags:
                if dataset.ul.button:
                    title = dataset.ul.button.text
                    titles.append(title)
                if pub_date_doc:
                    pub_date_doc = dataset.div.a.text
                    pub_date_docs.append(pub_date_doc)
        except:
            pass
    
    return titles, pub_date_docs


# TODO (Lee) categories: government-wide, system-wide, retired, general uses

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