# Blinkpy Snap

Leverages the [blinkpy](https://github.com/fronzbot/blinkpy) Python library to access a Blink 
camera system in order to take a picture with a single camera and then save it

## Usage

- `run.py` captures and downloads an image from a single camera which is then saved to a local 
path using sequential naming. Credentials are read from a configured or default path. If credentials 
are not found, the script can request them
  - Args:
    - `-c, --Camera`: Specifies the camera to activate
    - `-o, --Output`: Specifies the output path for captured images
    - `-a, --Auth`: Specifies the path to the credentials file (`credentials.json`)
    - `-q, --Quiet`: Enables quiet mode. Disables authentication prompts
  - Environment Variables
    - `Snap_Camera`: Maps to `-c`
    - `Snap_OutputPath`: Maps to `-o`
    - `Snap_AuthPath`: Maps to `-a`
- `session.py` is a wrapper around the initialization of a blinkpy `Blink` object 
which is consumed by `run.py`. This script may be run directly to reset your login credentials
- `Dockerfile` Executes `run.py` in quiet mode. Tip: Use environment variables for configuration
- `docker-compose.yaml` Executes `Dockerfile` with environment variable configuration and volume mounts

## Note

- Your Blink account credentials (username, password, session info), will be written to a 
local file `.blinkpy/credentials.json` upon running the sign in routine (`session.py`). Delete this file to remove 
them