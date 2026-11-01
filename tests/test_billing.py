import json
import pytest
from backend.stripe_service import StripeService
from backend.models import User, Subscription
from sqlalchemy import select


@pytest.mark.asyncio
async def test_stripe_service_checkout_session_mock():
    user = User(
        id="test-user-1234",
        github_id=12345678,
        username="vibe_hero",
        email="hero@vibe.dev",
    )
    res = await StripeService.create_checkout_session(user, plan="pro")
    assert "checkout_url" in res
    assert "session_id" in res
    assert "pro" in res["session_id"]


@pytest.mark.asyncio
async def test_stripe_webhook_completed_mock():
    # Setup in-memory sqlite session
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from backend.database import Base

    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSession = async_sessionmaker(bind=test_engine)
    async with TestSession() as session:
        user = User(id="u1", github_id=1, username="test_u1")
        sub = Subscription(user_id="u1", stripe_customer_id="cus_test_123", plan="free", status="active")
        session.add_all([user, sub])
        await session.commit()

        webhook_event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "customer": "cus_test_123",
                    "subscription": "sub_test_999",
                    "metadata": {"target_plan": "team", "user_id": "u1"},
                }
            },
        }

        payload = json.dumps(webhook_event).encode("utf-8")
        result = await StripeService.handle_webhook_payload(payload, sig_header="dummy", db=session)
        assert result["handled"] is True

        # Verify plan upgraded to team
        updated_sub = (await session.execute(select(Subscription).where(Subscription.user_id == "u1"))).scalar_one()
        assert updated_sub.plan == "team"
        assert updated_sub.stripe_subscription_id == "sub_test_999"
