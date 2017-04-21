#!/usr/bin/env python3

import json
import requests
import os
import os.path


if os.environ.get('SLACK_URL'):
    SLACK_URL = os.environ['SLACK_URL']
else:
    config_file = '{}/.plex_notify_config.json'.format(os.path.expanduser('~'))
    if not os.path.isfile(config_file):
        raise Exception(
            "No config file found in Environment Variables or at {}".format(config_file))
    config = json.load(open(config_file))
    SLACK_URL = config['slack_url']


def send_slack(msg):
    return requests.post(SLACK_URL, data=json.dumps(msg))


def process_event(event):
    msg = gen_msg(format_msg(event), format_viewer(event))
    response = send_slack(msg)
    print(response.status_code)


def format_title(meta):
    if 'grandparentTitle' in meta:
        return "{} S{}E{}: {}".format(meta['grandparentTitle'], meta['parentIndex'], meta['index'], meta['title'])
    else:
        return meta['title']


def format_viewer(event):
    return "{account} on {device} @ {ip}".format(account=event['Account']['title'], device=event['Player']['title'], ip=event['Player']['publicAddress'])


def format_msg(event):
    event_type = {
        'media.play': 'Started',
        'media.scrobble': 'Finished',
        'media.stop': 'Stopped',
        'media.rate': 'Rated',
    }
    return "{account} {type}: {title}".format(account=event['Account']['title'], type=event_type[event['event']], title=format_title(event['Metadata']))


def gen_msg(text, subtext):
    msg = {
        "text": text,
        "attachments": [
            {
                "text": subtext
            }
        ]
    }
    return msg


def main():
    sample = json.load(
        open('/Users/ndpete/dev/plexWebhook-integration/sample_tv_hook.json'))
    print(format_viewer(sample))
    print(format_title(sample['Metadata']))
    process_event(sample)


if __name__ == '__main__':
    main()
