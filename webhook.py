from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import stripe
import os

load_dotenv()

app = FastAPI()

stripe.api_key = os.getenv("STRIPE_API_KEY")
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'customer.subscription.created':
        subscription = event['data']['object']
        print("Subscription created:", subscription['id'])
        # Update database
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        print("Subscription deleted:", subscription['id'])
        # Update database accordingly

    return {"status": "success"}
