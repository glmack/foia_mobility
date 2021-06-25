def get_govwide_sorns():
    """Retrieve US government-wide system of records notices from fpc.gov"""
    import requests
    from bs4 import BeautifulSoup
    response = requests.get('https://www.fpc.gov/resources/SORNs/#container')
    soup = BeautifulSoup(response.content, 'html.parser')
    agency_el = soup.find_all('div', class_ = 'tabcontent')
    main_el = soup.find('section', id = 'main-content')
    dataset_els = main_el.find_all('button', class_ = 'usa-accordion__button text-primary-darker')
    for dataset_el in dataset_els:
        title = dataset_el.text
        print(title)

        
    
# list of datasets = ul class = usa-accordion usa-accordion--bordered
# dataset = li
# title = usa-accordion__button text-primary-darker # note double underscore

        # for dataset_tag in dataset_tags:
        #     if dataset_tag is not None:
        #         try:
        #             datasets.update(dataset_tag)
        #             datasets['title'] = dataset_tag.text
        #         except:
        #             pass
        #     else:
        #         pass
        # date_tag = agency_tag.findChildren('a')
        # datasets['title'].append(title_tag)
        # datasets['date'].append(date_tag)
        # datasets['agency'] = 
        
    return datasets

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