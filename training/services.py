import stripe
from training.models import Payments
from rest_framework.response import Response


class PaymentService:
    def create_payment(self, serializer, user):
        new_payment = serializer.save(user=user)

        stripe.api_key = 'sk_test_51OeDbXASb9i3kG2Vf4PrZ0b27t8CuJDWmGZ5NsjSr0vaRaJsMxndyH8msKKRYM9tEXJGvvscHjPTZvBJKdKxG3QP00vR0gmc1o'
        payment_intent = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            payment_method_types=["card"],
        )

        new_payment.session_id = payment_intent.id
        new_payment.amount = payment_intent.amount
        new_payment.save()


class PaymentService:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_payment(self, serializer, user):
        new_payment = serializer.save(user=user)

        stripe.api_key = self.api_key
        payment_intent = stripe.PaymentIntent.create(
            amount=2000,
            currency="usd",
            payment_method_types=["card"],
        )

        new_payment.session_id = payment_intent.id
        new_payment.amount = payment_intent.amount
        new_payment.save()