
def get_state_sorns():
    """Scrape list of record systems from Department of State website"""
# https://www.state.gov/system-of-records-notices-privacy-office/
    import requests
    url = 'https://www.state.gov/system-of-records-notices-privacy-office/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find('tbody')
    dataset_el = body.find_all('tr style')
    counter = 0
    datasets = []
    for dataset_el in dataset_els:
        if counter==0":
            pass
        else:
            fieldcounter = 1
            fields = dataset_el.findChildren('td')
            dataset_row = {['name': ]


