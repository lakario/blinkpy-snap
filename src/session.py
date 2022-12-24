import os.path
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load
import time


class BlinkSession:
    DEFAULT_AUTH_FILE = ".blinkpy/credentials.json"

    def __init__(
            self,
            auth_file: str = DEFAULT_AUTH_FILE
    ):
        self.auth_file = auth_file
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
        self._write_credentials()

        if with_sleep:
            time.sleep(3)

        return self.get(force_reset=False)

    def _write_credentials(self):
        # write auth file
        if not os.path.exists(os.path.dirname(self.auth_file)):
            os.makedirs(os.path.dirname(self.auth_file), exist_ok=True)
        self.blink.save(self.auth_file)
        print('Auth file updated: ' + self.auth_file)

    def get(self, force_reset=False, no_prompt=False):
        if force_reset or not self._auth_file_exists():
            print(f'Credentials not found. Searched: {self.auth_file}')
            if no_prompt:
                raise Exception("Credentials required. Unable to continue.")
            self.blink = self._refresh_auth(reset=True)
        else:
            print(f'Credentials located: {self.auth_file}')
            self.blink.auth = Auth(login_data=json_load(self.auth_file), no_prompt=True)
            self.blink.start()

            if not self.blink.available:
                return self._refresh_auth(reset=False)

        return self.blink


if __name__ == '__main__':
    BlinkSession().get(force_reset=True)
