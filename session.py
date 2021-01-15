import os.path
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load
import time

AUTH_FILE = "credentials.json"


class BlinkSession:

    def __init__(
            self
    ):
        self.auth_file = AUTH_FILE
        self.blink = Blink()

    def _auth_file_exists(self):
        return os.path.exists(self.auth_file)

    def _refresh_auth(self, reset=False):
        self.blink = Blink()
        with_sleep = False

        if not reset and self._auth_file_exists():
            self.blink.auth = Auth(json_load(self.auth_file))
            with_sleep = True
        else:
            self.blink.auth = Auth()

        self.blink.start()

        # write auth file
        self.blink.save(self.auth_file)
        print('Auth file updated: ' + self.auth_file)

        if with_sleep:
            time.sleep(3)

        return self.get(force_reset=False)

    def get(self, force_reset=False):
        if force_reset or not self._auth_file_exists():
            self.blink = self._refresh_auth(reset=True)
        else:
            self.blink.auth = Auth(login_data=json_load(self.auth_file), no_prompt=True)
            self.blink.start()

            if not self.blink.available:
                return self._refresh_auth(reset=False)

        return self.blink


if __name__ == '__main__':
    BlinkSession().get(force_reset=True)
