class PaymentGatewayUnreachable(Exception):
    """To be thrown when payment gateway is unreachable or errors out"""
    def __init__(self):
        super().__init__("Payment Gateway is down. Please try again later.")
