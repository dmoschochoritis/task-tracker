import json
import logging
import os
import sys
import time
import urllib.error
import urllib.request

API = os.environ.get("SIGNAGE_API", "http://localhost:8000")


def decide(status, body):
    if status == 404:
        return "Unknown screen"
    if body is None:
        return "No content assigned"
    return f"Playing {body['name']}: {', '.join(body['items'])}"

def fetch(screen_id):
    try:
        with urllib.request.urlopen(f"{API}/screens/{screen_id}/playlist", timeout=5) as res:
            return res.status, json.load(res)
    except urllib.error.HTTPError as err:
        return err.code, json.load(err)


def poll(screen_id, last):
    try:
        status, body = fetch(screen_id)
    except urllib.error.URLError:
        logging.warning("API unreachable, keeping last playlist")
        return last
    return decide(status, body)


def main():
    screen_id = int(sys.argv[1])
    last = None
    while True:
        current = poll(screen_id, last)
        if current != last:
            print(current, flush=True)
            last = current
        time.sleep(10)


if __name__ == "__main__":
    main()
