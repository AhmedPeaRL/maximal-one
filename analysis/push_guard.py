import os
import sys

if "GITHUB_ACTIONS" not in os.environ:
    print("❌ Push not allowed outside GitHub Actions")
    sys.exit(1)

token = os.getenv("GH_TOKEN")

if not token or len(token) < 20:
    print("❌ Invalid token")
    sys.exit(1)

print("✅ Push context verified")
