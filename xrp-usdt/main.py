BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"


def get_current_price():
    pass


def is_price_change():
    pass


def show_message():
    pass


def main():
    current_price = get_current_price()
    if is_price_change(current_price):
        show_message()


if __name__ == "__main__":
    main()
