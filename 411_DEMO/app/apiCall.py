import requests


def func(curr):
    url = "http://free.currencyconverterapi.com/api/v5/convert"
    querystring = {"q": curr + "_USD", "compact": "y"}

    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "4adcb384-9365-44c4-8793-705e86736b4b"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    return response.text
