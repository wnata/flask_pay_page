"""
piastrix
{
	"description": "Test Bill", - description
	"payer_currency": 643, - dictionary for currencies
	"shop_amount": "23.15", - pay_sum
	"shop_currency": 643,- dictionary for currencies
	"shop_id": "112", - static
	"shop_order_id": 4239, - order id from orders
	"sign": "ad7fbe8df102bc70e28deddba8b45bb3f4e6cafdaa69ad1ecc0e8b1d4e770575"
}

"""

"""
1. order from front
2. collecting data from order:
    description
    payer_currency
    shop_currency
    shop_amount
    shop_id
    shop_order_id

3. sign needs to be generated

need function that will have possibility to send request POST
 and will take url for redirect from response
"""

"""response = requests.post(
    'https://api.github.com/search/repositories',
    data={'key':'value'},
    headers={'Accept': 'application/vnd.github.v3.text-match+json'},
)"""

import requests

def cur_dict(currency):
    cur_cod = 0
    if currency.lower() == 'usd':
        cur_cod = 840
    elif currency.lower() == 'eur':
        cur_cod = 978
    else:
        cur_cod = 980
    
    return cur_cod


def pay_piastr(description, currency, shop_amount, order_id):
    data = {}
    
    data['description'] = description
    
    cur_code = cur_dict(currency)
    data['shop_currency'] = cur_code
    data['payer_currency'] = cur_code

    data['shop_amount'] = shop_amount
    data['shop_order_id'] = order_id

    data['shop_id'] = '112'

    data['sign'] = "ad7fbe8df102bc70e28deddba8b45bb3f4e6cafdaa69ad1ecc0e8b1d4e770575"

    url = 'https://core.piastrix.com/bill/create'

    headers = {
        "Content-Type": "application/json"
    }

    print(data)
    response = requests.post(url, json=data, headers=headers)
    #response.json()
    return response.json()