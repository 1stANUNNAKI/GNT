"""
Stripe Billing Service Module.
Handles customer creation, checkout session generation, and webhook lifecycle events.
"""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional
import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .models import Subscription, User


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """
    Manages monetized subscriptions (Free, Pro, Team) via Stripe Checkout & Billing.
    """

    PLAN_PRICES = {
        "pro": settings.STRIPE_PRICE_ID_PRO,
        "team": settings.STRIPE_PRICE_ID_TEAM,
    }

    @classmethod
    async def get_or_create_customer(cls, user: User, db: AsyncSession) -> str:
        """
        Retrieves existing Stripe Customer ID or registers a new one on Stripe.
        """
        # Check existing subscription record
        res = await db.execute(select(Subscription).where(Subscription.user_id == user.id))
        sub = res.scalar_one_or_none()

        if sub and sub.stripe_customer_id:
            return sub.stripe_customer_id

        # If Stripe key is configured, create customer on Stripe
        customer_id = f"cus_mock_{user.id[:8]}"
        if settings.STRIPE_SECRET_KEY:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.username,
                metadata={"user_id": user.id, "github_id": str(user.github_id)},
            )
            customer_id = customer.id

        if not sub:
            sub = Subscription(
                user_id=user.id,
                stripe_customer_id=customer_id,
                plan="free",
                status="active",
            )
            db.add(sub)
        else:
            sub.stripe_customer_id = customer_id

        await db.commit()
        return customer_id

    @classmethod
    async def create_checkout_session(
        cls,
        user: User,
        plan: str,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
        db: Optional[AsyncSession] = None,
    ) -> Dict[str, str]:
        """
        Generates a hosted Stripe Checkout URL for monthly subscriptions.
        """
        if plan not in cls.PLAN_PRICES:
            raise ValueError(f"Invalid plan '{plan}'. Choose from {list(cls.PLAN_PRICES.keys())}")

        customer_id = await cls.get_or_create_customer(user, db) if db else f"cus_mock_{user.id[:8]}"
        price_id = cls.PLAN_PRICES[plan]

        default_success = f"{settings.FRONTEND_URL}/dashboard?billing=success&session_id={{CHECKOUT_SESSION_ID}}"
        default_cancel = f"{settings.FRONTENDURL if hasattr(settings, 'FRONTENDURL') else settings.FRONTEND_URL}/pricing?billing=canceled"

        if settings.STRIPE_SECRET_KEY:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                mode="subscription",
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                success_url=success_url or default_success,
                cancel_url=cancel_url or default_cancel,
                metadata={"user_id": user.id, "target_plan": plan},
            )
            return {"checkout_url": session.url, "session_id": session.id}

        # Mock fallback for development / test mode without active Stripe API keys
        mock_id = f"cs_test_mock_{plan}_{user.id[:8]}"
        mock_url = f"{settings.FRONTEND_URL}/dashboard?billing=mock_success&plan={plan}"
        return {"checkout_url": mock_url, "session_id": mock_id}

    @classmethod
    async def create_portal_session(cls, user: User, return_url: Optional[str] = None, db: Optional[AsyncSession] = None) -> str:
        """
        Creates a Stripe Customer Portal link where subscribers can change payment methods or cancel.
        """
        customer_id = await cls.get_or_create_customer(user, db) if db else f"cus_mock_{user.id[:8]}"
        ret_url = return_url or f"{settings.FRONTEND_URL}/dashboard/settings"

        if settings.STRIPE_SECRET_KEY:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=ret_url,
            )
            return session.url

        return f"{settings.FRONTEND_URL}/dashboard/settings?portal=mock"

    @classmethod
    async def handle_webhook_payload(
        cls,
        payload_bytes: bytes,
        sig_header: str,
        db: AsyncSession,
    ) -> Dict[str, Any]:
        """
        Verifies Stripe webhook signature and synchronizes subscription states in PostgreSQL.
        """
        if settings.STRIPE_WEBHOOK_SECRET and settings.STRIPE_SECRET_KEY:
            try:
                event = stripe.Webhook.construct_event(
                    payload=payload_bytes,
                    sig_header=sig_header,
                    secret=settings.STRIPE_WEBHOOK_SECRET,
                )
            except Exception as e:
                raise ValueError(f"Webhook signature verification failed: {str(e)}")
        else:
            # Fallback parse for tests or unverified sandbox
            import json
            event = json.loads(payload_bytes.decode("utf-8"))

        event_type = event.get("type", "")
        data_object = event.get("data", {}).get("object", {})

        if event_type == "checkout.session.completed":
            customer_id = data_object.get("customer")
            subscription_id = data_object.get("subscription")
            target_plan = data_object.get("metadata", {}).get("target_plan", "pro")
            user_id = data_object.get("metadata", {}).get("user_id")

            if customer_id:
                query = select(Subscription).where(Subscription.stripe_customer_id == customer_id)
                res = await db.execute(query)
                sub = res.scalar_one_or_none()

                if sub:
                    sub.stripe_subscription_id = subscription_id
                    sub.plan = target_plan
                    sub.status = "active"
                    await db.commit()

        elif event_type in ("customer.subscription.updated", "customer.subscription.deleted"):
            customer_id = data_object.get("customer")
            status = data_object.get("status", "canceled")
            cancel_at_period_end = data_object.get("cancel_at_period_end", False)

            if customer_id:
                query = select(Subscription).where(Subscription.stripe_customer_id == customer_id)
                res = await db.execute(query)
                sub = res.scalar_one_or_none()

                if sub:
                    sub.status = "canceled" if status in ("canceled", "unpaid") else status
                    if status == "canceled":
                        sub.plan = "free"
                    await db.commit()

        return {"handled": True, "event_type": event_type}
