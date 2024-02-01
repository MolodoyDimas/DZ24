import stripe
from training.models import Payments
from rest_framework.response import Response

def perform_create(self, serializer):
    new_lesson = serializer.save()
    new_lesson.user = self.request.user
    new_payment = serializer.save()
    stripe.api_key = 'pk_test_51OeDbXASb9i3kG2Vf4PrZ0b27t8CuJDWmGZ5NsjSr0vaRaJsMxndyH8msKKRYM9tEXJGvvscHjPTZvBJKdKxG3QP00vR0gmc1o'
    payment_intent = stripe.PaymentIntent.create(
        amount=2000,
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )
    new_payment.session_id = payment_intent.id
    new_payment.amount = payment_intent.amount
    new_payment.save()

    return super().perform_create(new_payment)


def get(self, payment_id):
    payment = Payments.objects.get(pk=payment_id)
    payment_id = payment.session_id
    stripe.api_key = 'sk_test_51OdoXSHC8LUh8NqZQboynIwfP7znL7qfNqCOqOYkl7k3pzAKN8QU45ye5RpnABJ2MRjLBfk6tWWisTmY9QoiXJNR00NP3ImbNV'
    payment_intent = stripe.PaymentIntent.retrieve(payment_id)
    print(payment_intent)
    return Response({'status': payment_intent.status, 'body': payment_intent})