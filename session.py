import os.path
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load

AUTH_FILE = "credentials.json"


class BlinkSession:

    def __init__(
            self
    ):
        self.auth_file = AUTH_FILE
        self.blink = Blink()

    def _auth_exists(self):
        return os.path.exists(self.auth_file)

    def _refresh_auth(self, reset=False):
        if not reset and self._auth_exists():
            self.blink.auth = Auth(json_load(self.auth_file))

        self.blink.start()
        # update auth file
        self.blink.save(self.auth_file)

        return self.blink

    def get(self, force_refresh=False):
        if force_refresh or not self._auth_exists():
            self.blink = self._refresh_auth(True)
        else:
            self.blink.auth = Auth(login_data=json_load(self.auth_file), no_prompt=True)
            self.blink.start()

            if len(self.blink.cameras) == 0:
                self.blink = self._refresh_auth()

        return self.blink


if __name__ == '__main__':
    BlinkSession().get(force_refresh=True)
    print('Credentials updated')
