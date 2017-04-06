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
        raise Exception("No config file found in Environment Variables or at {}".format(config_file))
    config = json.load(open(config_file))
    SLACK_URL = config['slack_url']


def send_slack(msg):
    print(json.dumps(msg))
    r = requests.post(SLACK_URL, data=json.dumps(msg))
    print(r.status_code)
    print(r.headers)


def process_event(event):
    if event['event'] == 'media.play':
        msg = gen_msg(format_viewer(event), "Started: {}".format(format_title(event['Metadata'])))
        send_slack(msg)
    elif event['event'] == 'media.scrobble':
        msg = gen_msg(format_viewer(event), "Finished: {}".format(format_title(event['Metadata']))
        send_slack(msg)


def format_title(meta):
    if 'grandparentTitle' in meta:
        return "{} S{}E{}: {}".format(meta['grandparentTitle'], meta['parentIndex'], meta['index'], meta['title'])
    else:
        return meta['title']


def format_viewer(event):
    return "{account} on {device} @ {ip}".format(account=event['Account']['title'], device=event['Player']['title'], ip=event['Player']['publicAddress'])


def gen_msg(text, subtext):
    msg = {
        "text": text,
        "icon-emoji": ":plex:",
        "attachments": [
            {
                "text": subtext
            }
        ]
    }
    return msg


def main():
    sample = json.load(open('/Users/ndpete/dev/plexWebhook-integration/sample_tv_hook.json'))
    print(format_viewer(sample))
    print(format_title(sample['Metadata']))
    process_event(sample)


if __name__ == '__main__':
    main()
