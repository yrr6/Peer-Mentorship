# MongoDB Connection Test Script

## What This Does

- This is a basic Python script to test connecting to our MongoDB Atlas database.
- It uses PyMongo to "dial" the DB (URI with username/password).
- Prints fun messages like "Door opened!" if it connects and pings the server.
- If fails, says "Oops!" (e.g., wrong password or network issue).

## Why for Peer-Mentorship?

- MVP step for student login/register: Proves NoSQL setup works before adding users/hashes.
- Flexible for forum (posts/comments as JSON docs).
- Beginner-friendly—no frameworks, just connect + ping.

## How to Run

1. Install: `pip install pymongo` (in a venv).
2. Update `my_uri` with real Atlas password (don't commit secrets!).
3. Run: `python connection_test.py`

- Success: "Said hello—it's listening!" + "All done—hung up."
- Check in Atlas: Data persists in cloud.

## Next Steps

- Add hashing (bcrypt) for real passwords.
- Wrap in Flask for REST API (/login endpoint).
- Integrate with frontend forms.

Questions? Ping me!
