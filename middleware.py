import stripe
import os
from fastmcp.middleware import Middleware

stripe.api_key = os.getenv("STRIPE_API_KEY")

def get_customer_from_db(user_id):
    # Replace with your actual DB logic
    mock_db = {"user123": "cus_ABC123"}
    return mock_db.get(user_id)

class SubscriptionMiddleware(Middleware):
    def before_request(self, request):
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return {"error": "Unauthorized: No User ID"}, 401

        customer_id = get_customer_from_db(user_id)
        if not customer_id:
            return {"error": "Customer not found"}, 404

        subscriptions = stripe.Subscription.list(
            customer=customer_id, status="active"
        )
        if not subscriptions.data:
            return {"error": "No active subscription"}, 403

        return None  # proceed normally
