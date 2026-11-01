"""
Stripe Monetization and Billing Endpoints.
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import User
from ..schemas import (
    CheckoutSessionResponse,
    CreateCheckoutSessionRequest,
    CustomerPortalResponse,
)
from ..stripe_service import StripeService
from .auth import get_current_user


router = APIRouter(prefix="/api/billing", tags=["Billing & Monetization"])


@router.post("/create-checkout-session", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    req: CreateCheckoutSessionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Creates a Stripe Checkout session to upgrade to Pro ($12/mo) or Team ($29/mo).
    """
    try:
        res = await StripeService.create_checkout_session(
            user=user,
            plan=req.plan,
            success_url=req.success_url,
            cancel_url=req.cancel_url,
            db=db,
        )
        return CheckoutSessionResponse(checkout_url=res["checkout_url"], session_id=res["session_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/portal", response_model=CustomerPortalResponse)
async def get_customer_portal(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Redirects subscriber to Stripe Customer Portal to view invoices or cancel.
    """
    try:
        url = await StripeService.create_portal_session(user=user, db=db)
        return CustomerPortalResponse(portal_url=url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    db: AsyncSession = Depends(get_db),
):
    """
    Handles inbound Stripe webhook events to keep subscription states in sync.
    """
    payload_bytes = await request.body()
    try:
        result = await StripeService.handle_webhook_payload(
            payload_bytes=payload_bytes,
            sig_header=stripe_signature or "",
            db=db,
        )
        return {"received": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
