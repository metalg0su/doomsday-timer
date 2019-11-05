import datetime
from collections import namedtuple

import requests
from flask import Flask
from pytz import timezone

app = Flask(__name__)
TermData = namedtuple("Counter", "current_height, target_height, height_left,"
                                 "current_datetime, est_datetime,"
                                 "hours_left, minutes_left, seconds_left")

endpoint = "https://ctz.solidwallet.io/api/v3"
data = {
    "jsonrpc": "2.0",
    "method": "icx_call",
    "params": {
        "to": "cx0000000000000000000000000000000000000000",
        "dataType": "call",
        "data": {
            "method": "getIISSInfo"
        }
    },
    "id": 1
}


def get_data() -> dict:
    return requests.post(endpoint, json=data).json()


def parse_data(response: dict) -> TermData:
    current_height = int(response["result"]["blockHeight"], 16)
    target_height = int(response["result"]["nextPRepTerm"], 16)
    height_left = target_height - current_height

    t_diff = datetime.timedelta(seconds=height_left*2)
    curr_time = datetime.datetime.now(timezone("Asia/Seoul"))
    est_time = curr_time + t_diff

    hours, remainders = divmod(t_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainders, 60)

    return TermData(
        current_height=current_height, target_height=target_height, height_left=height_left,
        current_datetime=curr_time, est_datetime=est_time,
        hours_left=int(hours), minutes_left=int(minutes), seconds_left=int(seconds)
    )


def make_result(parsed_data: TermData):
    content0 = f">>> Current Height: {parsed_data.current_height}\n" \
              f">>> Target Height: {parsed_data.target_height} \n" \
              f">>> Heights left: {parsed_data.height_left} \n"
    content1 = f"... Current Time: {parsed_data.current_datetime} \n" \
               f"... Estimated Time: {parsed_data.est_datetime} \n"
    footer = f"... {parsed_data.hours_left} hours {parsed_data.minutes_left} minutes {parsed_data.seconds_left} seconds left."

    result_str = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Doomsday Timer"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content0
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/plants.png",
                    "alt_text": "plants"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content1
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
                        "alt_text": "notifications warning icon"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{footer}*"
                    }
                ]
            }
        ]
    }

    return result_str


@app.route('/', methods=["POST"])
def doomsday_counter():
    raw_data = get_data()
    parsed_data = parse_data(raw_data)
    result = make_result(parsed_data)

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
