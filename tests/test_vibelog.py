import pytest
from core.vibelog import VibeLog


def test_vibelog_features_and_fixes():
    diff_text = """
diff --git a/routes/billing.py b/routes/billing.py
new file mode 100644
--- /dev/null
+++ b/routes/billing.py
@@ -0,0 +1,5 @@
+from fastapi import APIRouter
+router = APIRouter()
+async def create_stripe_checkout():
+    pass
diff --git a/auth/login.py b/auth/login.py
--- a/auth/login.py
+++ b/auth/login.py
@@ -10,3 +10,5 @@
-    pass
+    try:
+        validate_token(token)
+    except Exception:
+        return False
"""
    summary = VibeLog.parse_diff(diff_text, commit_message="Fix login token validation")
    assert summary.total_files_changed == 2
    assert summary.total_lines_added > 0
    assert any("stripe" in f.lower() or "billing" in f.lower() for f in summary.features)
    assert any("safety shields" in fx.lower() or "login" in fx.lower() for fx in summary.fixes)
    assert summary.vibe_headline != ""

    md = summary.to_markdown()
    assert "## 📝 What changed?" in md
    assert "✨ New Features" in md
