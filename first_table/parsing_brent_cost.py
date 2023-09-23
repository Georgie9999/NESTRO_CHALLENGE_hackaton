from bs4 import BeautifulSoup
import requests
import pandas as pd
cost_table = pd.DataFrame(columns=["Date", "Brent_oil_cost"])
url = 'https://ru.investing.com/commodities/brent-oil-historical-data'
headers = {'user-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.findAll("tr", class_="h-[41px] hover:bg-[#F5F5F5] relative after:absolute after:bottom-0 after:bg-[#ECEDEF] after:h-px after:left-0 after:right-0 historical-data-v2_price__atUfP")
for el in rows:
      date = el.find("td", class_="datatable_cell__LJp3C text-left align-middle overflow-hidden text-v2-black text-ellipsis whitespace-nowrap text-sm font-semibold leading-4 min-w-[106px] left-0 sticky bg-white sm:bg-inherit").text
      cost = el.find("td", class_=lambda value: value and value.startswith("datatable_cell__LJp3C datatable_cell--align-end__qgxDQ")).text
      cost = str(cost).replace(',', '.')
      cost_table = pd.concat([cost_table, pd.Series({"Date": date, "Brent_oil_cost": cost}).to_frame().T], ignore_index=True)
cost_table['Brent_oil_cost'] = cost_table['Brent_oil_cost'].astype(float)
print(cost_table)