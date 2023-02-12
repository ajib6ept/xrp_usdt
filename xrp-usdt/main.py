import asyncio
import datetime
import json

import aiohttp

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"

TASKS_COUNT = 10
TTL_SEC = 60 * 60
PRICE_LIMIT = 1
REQUEST_TIMEOUT = 10


class BinanceUsdtDB:
    def __init__(self, ttl=TTL_SEC):
        self.ttl = ttl
        self.db = []

    def _remove_old_value(self):
        self.db = [
            item
            for item in self.db
            if (item[1] + datetime.timedelta(0, TTL_SEC))
            > datetime.datetime.now()
        ]

    def set_value(self, value, date):
        self._remove_old_value()
        self.db.append([value, date])
        print(f"set value {value} - {str(date)}")

    def get_max_value(self):
        return max(self.db, key=lambda x: x[0])


def show_message(price, max_price, limit):
    print(f"Price cahged {price}")


def is_price_change(current_value, max_value, limit):
    return 1 - current_value / max_value >= limit / 100


async def send_request(session, i, db):
    async with session.get(
        BINANCE_API_URL,
        raise_for_status=True,
        allow_redirects=False,
        timeout=REQUEST_TIMEOUT,
    ) as response:
        html = await response.text()
        usdt_price = json.loads(html)
        db.set_value(value=usdt_price, date=datetime.datetime.now())
        return usdt_price


async def main():
    db = BinanceUsdtDB()
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, i, db) for i in range(TASKS_COUNT)]
        results = await asyncio.gather(*tasks)
        max_price = db.get_max_value()
        for price in results:
            if is_price_change(price, max_price, limit=PRICE_LIMIT):
                show_message(price, max_price, limit=PRICE_LIMIT)


if __name__ == "__main__":
    while True:
        asyncio.run(main())
