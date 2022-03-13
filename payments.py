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
import hashlib
import json

def cur_dict(currency):
    cur_cod = 0
    if currency.lower() == 'usd':
        cur_cod = 840
    elif currency.lower() == 'eur':
        cur_cod = 978
    else:
        cur_cod = 643

    return cur_cod


def gen_sign(currency, shop_amount, order_id):
    secret_key = 'SecretKey01'
    shop_id = '5'

    str = f'{cur_dict(currency)}:{shop_amount}:{cur_dict(currency)}:{shop_id}:{order_id}{secret_key}'
    hash_object = hashlib.sha256(str.encode())

    return hash_object.hexdigest()


def pay_piastr(description, currency, shop_amount, order_id):
    data = {}

    data['description'] = description

    cur_code = cur_dict(currency)
    data['shop_currency'] = cur_code
    data['payer_currency'] = cur_code

    data['shop_amount'] = shop_amount
    data['shop_order_id'] = order_id

    data['shop_id'] = '5'

    data['sign'] = gen_sign(currency, shop_amount, order_id)

    url = 'https://core.piastrix.com/bill/create'

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)
    url = response.json()
    print(response.json())
    print (url['data']['url'])
    return url['data']['url']
