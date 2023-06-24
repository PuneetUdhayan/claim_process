class PaymentGatewayUnreachable(Exception):
    def __init__(self):
        super().__init__("Payment Gateway is down. Please try again later.")
