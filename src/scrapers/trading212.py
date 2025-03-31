import json
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape():
    url = "https://www.trading212.com/trading-instruments/invest"

    result = {}

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Extract data
    data = driver.find_element(By.ID, '__NEXT_DATA__')
    # We need to use special attribute instead of data.text because this is <script> element
    data = data.get_attribute('textContent')
    # Encode JSON
    data = json.loads(data)

    driver.quit()

    # Get lists
    """
    {
        "id": 54,
        "countryCode": "DE",
        "readableCaption": "Deutsche Börse Xetra"
    }
    """
    exchanges = data['props']['pageProps']['workingSchedules']
    exchanges = {exchange['id']: exchange for exchange in exchanges}

    """
    {
        "ticker": "00XJ1d_EQ",
        "type": "ETF",
        "isin": "JE00B78NPY84",
        "currency": "EUR",
        "shortName": "00XJ",
        "fullName": "WisdomTree Agriculture - EUR Daily Hedged",
        "description": "WisdomTree Agriculture - EUR Daily Hedged",
        "countryOfOrigin": "JE",
        "minTrade": 0.2,
        "digitsPrecision": 4,
        "quantityPrecision": 8,
        "exchangeId": 166,
        "tradable": true,
        "underlyingInstrumentTicker": "00XJ1d_EQ",
        "underlyingLeverageCoefficient": 1,
        "dealerExclusions": [
            "T212AU"
        ],
        "maxOpenLong": 50000000,
        "isaIneligible": false,
        "extendedHoursTradingEnabled": false,
        "enabledTradingSessions": "REGULAR",
        "subclasses": [
            "EXCHANGE_TRADED_COMMODITY"
        ]
    }
    """
    instruments = data['props']['pageProps']['instruments']['items']

    # Loop over instruments
    for instrument in instruments:
        ticker = instrument['ticker']
        isin = instrument['isin']
        name = instrument['fullName']
        description = instrument['description']
        countryOfOrigin = instrument['countryOfOrigin']
        tradable = instrument['tradable']
        type = instrument['type']
        isaIneligible = instrument['isaIneligible']
        exchangeId = instrument['exchangeId']

        if tradable == False:
            continue

        exchange = exchanges[exchangeId]
        countryOfExchange = exchange['countryCode']

        resultKey = ticker + ':' + str(exchangeId)

        # Add to result
        result[resultKey] = {
            'ticker': ticker,
            'isin': isin,
            'name': name,
            'description': description,
            'countryOfOrigin': countryOfOrigin,
            'countryOfExchange': countryOfExchange,
            'isEtf': type == 'ETF',
            'isaAvailable': isaIneligible == False,
        }

    return result