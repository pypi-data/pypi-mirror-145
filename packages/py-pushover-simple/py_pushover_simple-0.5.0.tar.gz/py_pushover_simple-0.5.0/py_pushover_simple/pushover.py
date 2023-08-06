"""Python Pushover API wrapper

Python module to access the Pushover <https://pushover.net> API.
Recommended: Python 3 or later

"""

import argparse
import os.path
import json
import requests


def arg_parse():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-u', '--user_key', metavar='<string>', help='pushover user token')
    parser.add_argument(
        '-t', '--app_token', metavar='<string>', help='pushover app token')
    return parser.parse_args()


class PushoverError(Exception):
    """Pushover API error"""


class Pushover:
    """A connection to the Pushover API

    Raises:
        PushoverError: Pushover API error
    """
    def __init__(self, user=None, token=None, sound=None,
                 target=None, url=None, url_title=None,
                 title=None, priority=0, timestamp=None,
                 retry=None, expire=None,):
        self.url = url
        self.user = user
        self.sound = sound
        self.title = title
        self.token = token
        self.target = target
        self.priority = priority
        self.timestamp = timestamp
        self.url_title = url_title
        self.retry = retry
        self.expire = expire

    def send_message(self, message):
        """Send a message using the Pushover API."""

        url = "https://api.pushover.net/1/messages.json"
        r = requests.post(url, data={
                        "url": self.url,
                        "user": self.user,
                        "sound": self.sound,
                        "title": self.title,
                        "token": self.token,
                        "device": self.target,
                        "message": message,
                        "priority": self.priority,
                        "timestamp": self.timestamp,
                        "url_title": self.url_title,
                        "retry": self.retry,
                        "expire": self.expire,
        }, headers={"Content-type": "application/x-www-form-urlencoded"}
        )
        output = r.text
        data = json.loads(output)

        if data['status'] != 1:
            raise PushoverError(output)

        return True


def debug():
    """Debug module."""
    args = arg_parse()

    user_key_set = args.user_key or args.user_key == ""
    app_token_set = args.app_token or args.app_token == ""

    print(user_key_set)
    print(app_token_set)

    if not user_key_set or not app_token_set:
        # Handle this better... If not set, ask user.
        print("Set user key and token with -u and -t respectively.")
        print("Exiting...")
        exit()
    else:
        user = args.user_key
        token = args.app_token

    p = Pushover()
    p.user = user
    p.token = token
    p.title = os.path.basename(__file__)
    p.send_message("Testing pushover.py...")


if __name__ == '__main__':
    debug()
