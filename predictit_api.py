import time
import pandas as pd
import requests
import os


def get_all_markets():
    time.sleep(5)
    url = "https://www.predictit.org/api/marketdata/all/"
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 "
                      "Safari/537.36",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-platform": "Windows",
        "accept-encoding": "gzip, deflate, br",
        "access-control-allow-origin": "*",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-fetch-dest": "empty",
        "content-type": "application/json",
    }
    response = requests.get(url, headers=headers).json()
    print(response)
    markets = response['markets']
    df_markets = pd.DataFrame(markets)
    df_markets = df_markets[["id", "shortName", "contracts", "timeStamp", "status"]]
    return df_markets


def unpack_contracts(event_id, data=pd.DataFrame(get_all_markets())):
    df_data = data.copy()
    df_data = df_data[df_data["id"] == event_id]
    row = df_data.iloc[0]
    event_name = row['shortName']
    contracts = row['contracts']
    df_output = pd.DataFrame(columns=["event_id", "eventName", "contract_id", "shortName", 'lastTradePrice',
                                      'bestBuyYesCost', 'bestBuyNoCost', 'bestSellYesCost', 'bestSellNoCost',
                                      'lastClosePrice'])
    for x in contracts:
        contract_id = x['id']
        short_name = x['shortName']
        last_trade = x['lastTradePrice']
        bestBuyYes = x['bestBuyYesCost']
        bestBuyNo = x['bestBuyNoCost']
        bestSellYes = x['bestSellYesCost']
        bestSellNo = x['bestSellNoCost']
        lastClosePrice = x['lastClosePrice']
        df_output.loc[len(df_output.index)] = [event_id, event_name, contract_id, short_name, last_trade, bestBuyYes, bestBuyNo, bestSellYes, bestSellNo, lastClosePrice]
    return df_output


def get_all_contracts():
    df_data = get_all_markets()
    data = df_data.copy()
    id_list = df_data["id"].tolist()
    df_all = pd.DataFrame()
    for x in id_list:
        df_temp = unpack_contracts(x, data)
        df_all = pd.concat([df_all, df_temp], ignore_index=True)
        df_all.loc[len(df_all.index)] = ["", "", "", "", "", "", "", "", "", ""]
    return df_all


def get_balance():
    token = os.getenv("token")
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 "
                      "Safari/537.36",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-platform": "Windows",
        "accept-encoding": "gzip, deflate, br",
        "access-control-allow-origin": "*",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-fetch-dest": "empty",
        "content-type": "application/json",
        "authorization": token
    }
    url = "https://www.predictit.org/api/User/Wallet/Balance"
    response = requests.get(url, headers=headers).json()
    return response
