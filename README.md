# Whyvo Call Backend Clean

Clean call signaling backend for Whyvo native audio/video calling.

## Included
- invite
- poll
- accept
- decline
- end
- Agora RTC token generation

## Excluded
- donor call runtime
- old signaling protocols
- frontend secret exposure

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
