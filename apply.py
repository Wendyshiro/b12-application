import hashlib
import hmac
import json
from datetime import datetime, timezone

import requests

#configuration
NAME = "Wendy Wanjiru Waweru"
Email = "wendywanjiru18@gmail.com"
RESUME_LINK = "https://docs.google.com/document/d/1O14HkixkYVtxfA_Jg6W-wQYIbTy2DlF_/edit"
SIGNING_SECRET = "hello-there-from-b12"
ENDPOINT = "https://b12.io/apply/submission"

#These will be set after repo creation
REPOSITORY_LINK = "https://github.com/Wendyshiro/b12-application"
ACTION_RUN_LINK = "https://github.com/Wendyshiro/b12-application/actions/runs/PLACEHOLDER"


def build_payload(action_run_link: str) -> str:
    """Build canonicalized JSON payload - keys sorted, no extra whitespace."""
    payload = {
        "action_run_link": action_run_link,
        "email": EMAIL,
        "name": NAME,
        "repository_link": REPOSITORY_LINK,
        "resume_link": RESUME_LINK,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") +
                     f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z",
                
    }
    #Compact separators, keys already sorted alphabetically in dict above
    return json.dumps(payload, separators=(",",":"), sort_keys=True)

def sign_payload(payload: str) -> str:
    """Generate HMAC-SHA256 signature."""
    secret = SIGNING_SECRET.encode("utf-8")
    body = payload.encode("utf-8")
    digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"

def submit(action_run_link: str) -> None:
    payload = build_payload(action_run_link)
    signature = sign_payload(payload)

    print(f"Submitting application for {NAME}...")
    print(f"Payload: {payload}")
    print(f"Signature: {signature}")

    respone = request.post(
        ENDPOINT,
        data=payload.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": signature.
        },
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        if data.get("Success"):
            print(f"\n✅ Application submitted successfully!")
            print(f"Receipt: {data['receipt']}")
        else:
            print("❌ Submission failed:", response.text)
    else:
        print("❌ HTTP error:", response.status_code, response.text)


if __name__ == "__main__":
    import os
    #In GHA the run URL is available via environment
    action_run_link = os.environ.get("ACTION_RUN_LINK", ACTION_RUN_LINK)
    submit(action_run_link)
    




