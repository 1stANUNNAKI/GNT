import pytest
from core.secrets import SecretShield, Severity


@pytest.fixture
def shield():
    return SecretShield()


def test_detect_openai_key(shield):
    fake_diff = """
diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,3 +1,4 @@
 import os
+OPENAI_API_KEY = "sk-proj-abc1234567890abcdef1234567890abcdef123456"
 print("Starting app")
"""
    findings = shield.scan_git_diff(fake_diff)
    assert len(findings) == 1
    assert findings[0].rule_id == "OPENAI_KEY"
    assert findings[0].severity == Severity.CRITICAL
    assert findings[0].file_path == "app.py"
    assert findings[0].line_number == 2
    assert "sk-p" in findings[0].masked_value
    assert "*" in findings[0].masked_value


def test_detect_stripe_key(shield):
    code = 'const stripeKey = "sk_live_51Abcdefghijklmnopqrstuvwx123456";'
    findings = shield.scan_text(code, file_path="config.js")
    assert len(findings) == 1
    assert findings[0].rule_id == "STRIPE_SECRET_KEY"
    assert findings[0].severity == Severity.CRITICAL


def test_detect_aws_access_key(shield):
    code = 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"'
    findings = shield.scan_text(code, file_path="deploy.py")
    assert any(f.rule_id == "AWS_ACCESS_KEY_ID" for f in findings)


def test_detect_forbidden_file_tracked(shield):
    finding = shield.audit_file_path(".env")
    assert finding is not None
    assert finding.rule_id == "FORBIDDEN_FILE_TRACKED"
    assert finding.severity == Severity.CRITICAL

    finding_nested = shield.audit_file_path("backend/.env.local")
    assert finding_nested is not None
    assert finding_nested.rule_id == "FORBIDDEN_FILE_TRACKED"


def test_shannon_entropy_calculation(shield):
    low_entropy = "aaaaaaaaaaaaaaaaaaaa"
    high_entropy = "h8Q2!v$91z@K4m*L7p#W9x~0"
    low_val = shield.calculate_shannon_entropy(low_entropy)
    high_val = shield.calculate_shannon_entropy(high_entropy)
    assert low_val == 0.0
    assert high_val > 4.0


def test_high_entropy_secret_assignment(shield):
    code = 'secret_token = "qW9$kL2#zX7!vB4@mN8*pT1~"'
    findings = shield.scan_text(code, file_path="auth.py")
    assert len(findings) >= 1
    assert any(f.rule_id == "HIGH_ENTROPY_TOKEN" for f in findings)


def test_mask_secret(shield):
    masked = shield.mask_secret("sk-1234567890abcdef123456")
    assert masked.startswith("sk-1")
    assert masked.endswith("456")
    assert "*" in masked
