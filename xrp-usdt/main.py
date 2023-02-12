import asyncio
import datetime
import json
from typing import List, Tuple

import aiohttp

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"

TASKS_COUNT = 10
TTL_SEC = 60 * 60
PRICE_LIMIT = 1
REQUEST_TIMEOUT = 10


class BinanceUsdtDB:
    def __init__(self, ttl: int = TTL_SEC) -> None:
        self.ttl = ttl
        self.db: List[Tuple[float, datetime.datetime]] = []

    def _remove_old_value(self) -> None:
        self.db = [
            item
            for item in self.db
            if (item[1] + datetime.timedelta(0, TTL_SEC))
            > datetime.datetime.now()
        ]

    def set_value(self, value: float, date: datetime.datetime) -> None:
        self._remove_old_value()
        self.db.append((value, date))
        print(f"set value {value} - {str(date)}")

    def get_max_value(self) -> float:
        return max(self.db, key=lambda x: x[0])[0]


def show_message(price: float, max_price: float, limit: int) -> None:
    print(f"Price cahged {price}")


def is_price_change(
    current_value: float, max_value: float, limit: int
) -> bool:
    return 1 - current_value / max_value >= limit / 100


async def send_request(
    session: aiohttp.ClientSession, db: BinanceUsdtDB
) -> float:
    async with session.get(
        BINANCE_API_URL,
        raise_for_status=True,
        allow_redirects=False,
        timeout=REQUEST_TIMEOUT,
    ) as response:
        html = await response.text()
        usdt_price = float(json.loads(html)["price"])
        db.set_value(value=usdt_price, date=datetime.datetime.now())
        return usdt_price


async def main() -> None:
    db = BinanceUsdtDB()
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, db) for _ in range(TASKS_COUNT)]
        results = await asyncio.gather(*tasks)
        max_price = db.get_max_value()
        for price in results:
            if is_price_change(price, max_price, limit=PRICE_LIMIT):
                show_message(price, max_price, limit=PRICE_LIMIT)


if __name__ == "__main__":
    while True:
        asyncio.run(main())
