import currencyapicom
import aiohttp
from bs4 import BeautifulSoup as bs
from collections import OrderedDict


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


class Weather:
    @staticmethod
    async def get_weather():
        url = "https://weather.com/ru-RU/weather/tenday/l/Almaty+Kazakhstan?canonicalCityId=e25e2b869e6e01f6f1fa4ab6b563313212c9718a0d78156ed8014563ba77c7dc"
        response = await fetch(url)
        soup = bs(response, "html.parser")
        dates = await Weather.get_dates(soup)
        high_temps = await Weather.get_high_temps(soup)
        low_temps = await Weather.get_low_temps(soup)
        conditions = await Weather.get_conditions(soup)
        data = []
        for date, high_temp, low_temp, condition in zip(
            dates, high_temps, low_temps, conditions
        ):
            data.append(
                {
                    "date": date,
                    "high_temp": high_temp,
                    "low_temp": low_temp,
                    "condition": condition,
                }
            )
        return data

    @staticmethod
    async def get_dates(soup):
        class_ = "DailyContent--daypartDate--3VGlz"
        data = [x.text for x in soup.find_all("span", class_=class_)]
        return list(OrderedDict.fromkeys(data))

    @staticmethod
    async def get_high_temps(soup):
        class_ = "DetailsSummary--highTempValue--3PjlX"
        return [x.text for x in soup.find_all("span", class_=class_)]

    async def get_low_temps(soup):
        class_ = "DetailsSummary--lowTempValue--2tesQ"
        return [x.text for x in soup.find_all("span", class_=class_)]

    async def get_conditions(soup):
        class_ = "DetailsSummary--extendedData--307Ax"
        return [x.text for x in soup.find_all("span", class_=class_)]


class CurrencyRate:
    @staticmethod
    async def get_currency_rate(filter=()):
        url = "https://www.mig.kz/"
        response = await fetch(url)
        soup = bs(response, "html.parser")
        currencies = await CurrencyRate.get_currencies(soup)
        buy_prices = await CurrencyRate.get_buy_prices(soup)
        sell_prices = await CurrencyRate.get_sell_prices(soup)
        data = []
        for currency, buy_price, sell_price in zip(currencies, buy_prices, sell_prices):
            if not filter or currency in filter:
                data.append(
                    {
                        "currency": currency,
                        "buy_price": buy_price,
                        "sell_price": sell_price,
                    }
                )
        return data

    @staticmethod
    async def get_currencies(soup):
        class_ = "currency"
        return [x.text for x in soup.find_all("td", class_=class_)]

    @staticmethod
    async def get_buy_prices(soup):
        class_ = "buy"
        return [x.text for x in soup.find_all("td", class_=class_)]

    @staticmethod
    async def get_sell_prices(soup):
        class_ = "sell"
        return [x.text for x in soup.find_all("td", class_=class_)]


class CurrencyRateAPI:
    @staticmethod
    async def get_currency_rate():
        client = currencyapicom.Client(
            "cur_live_t6Uucj5DX8VBEYUra2lX9OGCEVednBdwOKy70Ngl"
        )
        usd = round(client.latest("USD", currencies=["KZT"])["data"]["KZT"]["value"], 2)
        eur = round(client.latest("EUR", currencies=["KZT"])["data"]["KZT"]["value"], 2)
        rub = round(client.latest("RUB", currencies=["KZT"])["data"]["KZT"]["value"], 2)
        return [{"USD": usd}, {"EUR": eur}, {"RUB": rub}]
