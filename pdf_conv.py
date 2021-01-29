import tabula
import requests
import pandas as pd

filepath = '/Users/lee/Documents/code/foia_mobility/TRip_Relocation.pdf'

response = requests.get('https://d2d.gsa.gov/report/gsa-ogp-business-travel-and-relocation-dashboard')

dfs = tabula.read_pdf(filepath, multiple_tables=True, pages=8)
total_2019 = dfs[1]
fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
ax.table(cellText=total_2019.values, colLabels=total_2019.columns, loc='center')
fig.tight_layout()
plt.show()

# make api call to us gov gsa regulations api
response = requests.get('https://api.regulations.gov/v4/comments?filter[searchTerm]=travel&api_key=DEMO_KEY')