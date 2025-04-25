import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

base_url = "https://www.expatistan.com/cost-of-living/abuja"
cost_of_living = []

response = requests.get(base_url)
website_html = response.text

soup = BeautifulSoup(website_html, 'lxml')

item_names = soup.find_all(name='a', class_='downlighted')
item_prices = soup.find_all(name='td', class_='price city-1')

goods_name = [item.getText() for item in item_names]
goods_price = [price.getText() for price in item_prices]

for item in len(goods_name):
    for price in goods_price:
        if price == '\n':
            continue
        else:
            cost_of_living.append({
                'item': item,
                'price': price
            })

print(goods_name)
print(goods_price)

df = pd.DataFrame(cost_of_living)
df.to_csv('items.csv', index=False)
print("completed, saved to csv file")
