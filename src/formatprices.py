def format_prices(price):
    price = price.__format__('0.2f')
    price = price.replace(".", ",")
    return f"{price} €"