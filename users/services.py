import stripe


from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_API_KEY


# def create_stripe_product():
#     """Создание продукта в страйпе."""
#     product = stripe.Product.create(name="Gold Plan")
#     return product
#
# def convert_rub_to_dollars(amount):
#     """
#         Конвертирует рубли в доллары.
#         :param amount:
#         :return:
#     """
#     c = CurrencyRates()
#     rate = c.get_rate('RUB', 'USD')
#     return int(amount * rate)
#
#
# def create_stripe_price(amount):
#     """
#     Создание цены в страйпе
#     :param amount:
#     :return:
#     """
#
#     return stripe.Price.create(
#         currency="rub",
#         unit_amount=amount * 100,
#         product_data={"name": "Payment"},
#     )
#
# def create_stripe_session(price):
#     """
#         Создание сессию на оплату в страйпе.
#         :param price:
#         :return:
#     """
#     session = stripe.checkout.Session.create(
#         success_url="https://127.0.0.1:8000/",
#         line_items=[{"price": price.get("id"), "quantity": 1}],
#         mode="payment",
#     )
#     return session.get("id"), session.get("url")


def create_payment_link(amount, product_name):
    """Простая функция создания платежной ссылки"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': product_name,
                    },
                    "unit_amount": int(amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://127.0.0.1:8000/users/payments/success/",
            cancel_url="https://127.0.0.1:8000/users/payments/cancel/",
        )
        return session.url, session.id
    except Exception as e:
        return None, str(e)
