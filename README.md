# Blinkpy Snap

Leverages the [blinkpy](https://github.com/fronzbot/blinkpy) Python library to access a Blink 
camera system in order to take a picture with a single camera and then save it.

## Usage

- `run.py` contains a simple script to pull an image from a camera called 'Farm' which will be 
saved to a local path 'images' using sequential naming. If credentials are required, they will 
be requested and then stored locally.
- `session.py` contains is a wrapper around the initialization of a blinkpy `Blink` object 
which is consumed by run.py. This script may be run directly to reset your login credentials.

## Note

- Your Blink account credentials (username, password, session info), will be written to a 
local file `credentials.json` upon running the sign in routine. Delete this file to remove 
them.