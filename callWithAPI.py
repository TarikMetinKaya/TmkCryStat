import json
import ccxt
import ignoreConfig #Create a Python file named like "ignoreConfig.py"
import pathGetter
from pandas import DataFrame

binance_client=ccxt.binance({
    'apiKey':ignoreConfig.BINANCE_KEY,
    'secret':ignoreConfig.BINANCE_SECRET_KEY
})




def Get_Close_Of_Ticker(Symbol):
    return binance_client.fetchTicker(Symbol)['close']


def Get_Balance_As_Dataframe():
    balance=binance_client.fetch_balance()
    currNameList=[]
    currAmountList=[]
    for curr in balance['info']['balances']:
        if (float(curr['free']) + float(curr['locked'])) != 0:
            currNameList.append(curr['asset'])
            currAmountList.append(( float(curr['free']) + float(curr['locked']) ))
    return DataFrame(list(zip(currNameList,currAmountList)),
                     columns=['name','amount'])


def Get_Balance_USD_As_Dataframe():
    df=Get_Balance_As_Dataframe()
    priceOfBTC=Get_Close_Of_Ticker("BTC/USDT")
    priceOfBNB=Get_Close_Of_Ticker("BNB/USDT")
    priceOfETH=Get_Close_Of_Ticker("ETH/USDT")
    priceOfBUSD=Get_Close_Of_Ticker("BUSD/USDT")
    balanceList=[]

    for i in range(0,len(df['name'])):
        try:
            if df['name'][i]=="USDT":
                balance=df['amount'][i]
            else:
                price=Get_Close_Of_Ticker(f"{df['name'][i]}/USDT")
                balance=price*df['amount'][i]
        except:
            try:
                price=Get_Close_Of_Ticker(f"{df['name'][i]}/BUSD")
                balance=price*df['amount'][i]*priceOfBUSD
            except:
                try:
                    price = Get_Close_Of_Ticker(f"{df['name'][i]}/BTC")
                    balance = price * df['amount'][i] * priceOfBTC
                except:
                    try:
                        price = Get_Close_Of_Ticker(f"{df['name'][i]}/BNB")
                        balance = price * df['amount'][i] * priceOfBNB
                    except:
                        try:
                            price = Get_Close_Of_Ticker(f"{df['name']}/ETH")
                            balance = price * df['amount'][i] * priceOfETH
                        except:
                            balance=0
        print(df['name'][i])
        print(balance)
        balanceList.append(balance)

    df['balance']=balanceList
    return df


# print(binance_client.has)
# if (binance_client.has['fetchClosedOrders']):
#     c=binance_client.fetchClosedOrders (symbol="HOTETH")
#     print(c)

#print(Get_Balance_As_Dict())



print(Get_Balance_USD_As_Dataframe())


