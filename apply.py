import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

import requests

NAME = "Wendy Wanjiru Waweru"
EMAIL = "wendywanjiru18@gmail.com"
RESUME_LINK = "https://docs.google.com/document/d/1O14HkixkYVtxfA_Jg6W-wQYIbTy2DlF_/edit?usp=sharing&ouid=100519935744653555409&rtpof=true&sd=true"
REPOSITORY_LINK = "https://github.com/Wendyshiro/b12-application"
SIGNING_SECRET = "hello-there-from-b12"
ENDPOINT = "https://b12.io/apply/submission"


def build_payload(action_run_link):
    now = datetime.now(timezone.utc)
    ms = now.microsecond // 1000
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{ms:03d}Z"

    payload = {
        "action_run_link": action_run_link,
        "email": EMAIL,
        "name": NAME,
        "repository_link": REPOSITORY_LINK,
        "resume_link": RESUME_LINK,
        "timestamp": timestamp,
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def sign_payload(payload):
    secret = SIGNING_SECRET.encode("utf-8")
    body = payload.encode("utf-8")
    digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
    return "sha256=" + digest


def submit(action_run_link):
    payload = build_payload(action_run_link)
    signature = sign_payload(payload)

    print("Submitting application for " + NAME)
    print("Payload: " + payload)
    print("Signature: " + signature)

    response = requests.post(
        ENDPOINT,
        data=payload.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": signature,
        },
    )

    print("Status: " + str(response.status_code))
    print("Response: " + response.text)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print("Application submitted successfully!")
            print("Receipt: " + data["receipt"])
        else:
            print("Submission failed: " + response.text)
    else:
        print("HTTP error: " + str(response.status_code) + " " + response.text)


action_run_link = os.environ.get("ACTION_RUN_LINK", REPOSITORY_LINK + "/actions")
submit(action_run_link)