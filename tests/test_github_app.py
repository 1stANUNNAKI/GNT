import hashlib
import hmac
import pytest
from github_app.webhook_handler import GitHubWebhookHandler


@pytest.fixture
def webhook_handler():
    return GitHubWebhookHandler(webhook_secret="test_secret_12345")


def test_verify_signature_valid(webhook_handler):
    payload = b'{"action": "opened", "pull_request": {"number": 1}}'
    mac = hmac.new(b"test_secret_12345", msg=payload, digestmod=hashlib.sha256).hexdigest()
    sig_header = f"sha256={mac}"

    assert webhook_handler.verify_signature(payload, sig_header) is True


def test_verify_signature_invalid(webhook_handler):
    payload = b'{"action": "opened"}'
    sig_header = "sha256=invalid_hash_value"
    assert webhook_handler.verify_signature(payload, sig_header) is False
    assert webhook_handler.verify_signature(payload, None) is False


@pytest.mark.asyncio
async def test_handle_unknown_event(webhook_handler):
    result = await webhook_handler.handle_event("star", {})
    assert result["status"] == "ignored"


@pytest.mark.asyncio
async def test_handle_push_event(webhook_handler):
    result = await webhook_handler.handle_event("push", {"commits": [{"id": "abc"}]})
    assert result["status"] == "processed"
    assert result["commits_evaluated"] == 1
