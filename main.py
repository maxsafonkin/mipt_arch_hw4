import converter


def get_amount() -> int | None:
    amount_str = input("Введите значение в USD: \n")
    try:
        return int(amount_str)
    except ValueError:
        msg_err = f"Неверное количество валюты: {amount_str}"
        print(msg_err)
        return None


def get_currency() -> converter.structures.Currency | None:
    currency_str = input("Введите валюту: \n")
    try:
        return converter.structures.Currency(currency_str)
    except ValueError:
        msg_err = f"Неверное значение валюты: {currency_str}"
        print(msg_err)
        return None


def main() -> None:
    rates_provider = converter.RatesProvider(
        config=converter.RatesProviderConfig(
            url="https://api.exchangerate-api.com/v4/latest/USD",
            cache_expiry=60,
            max_retries=3,
            retry_delay=5,
            timeout=30,
        )
    )
    currency_converter = converter.CurrencyConverter(rates_provider=rates_provider)

    if (amount := get_amount()) is None or (currency := get_currency()) is None:
        return

    converted_amount = currency_converter.convert(amount, currency)
    msg_info = f"{amount} USD to {currency}: {converted_amount}"
    print(msg_info)


if __name__ == "__main__":
    main()
