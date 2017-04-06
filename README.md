# Plex Notify
Simple python app to listen for Plex Webhooks and relay events to slack channnel

## Disclaimer
This is super rough first draft. I'm using the project to better understand API's, Webhooks, python, and everything in between. The current listener is probably best just for testing environments.

Future aspirations is to use AWS API Gateway and a AWS lambda for notifications

### If you are looking for something more refined check Plex's example app [here](https://github.com/plexinc/webhooks-slack)

Events Currently Supported:
- media.play
- media.scrobble

## Setup
1. Create a Slack Incoming Webhook and copy url to Environment Variable `SLACK_URL` or create config file at `~/.plex_notify_config.json`
2. Add Plex Webhook to IP running the app see [here](https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks) for instructions
3. Clone the repo
4. Install python requirements `pip install -r requirements.txt` should only need `flask` and `requests`
5. From the repo directory Start listener: `python3 listener.py`
4. Start watching and look for a message

### Example Config File:
```json
{
  "slack_url": "URL HERE"
}
```

## TODOs
- Add more events
- Listener: Handle image attachments for the webhooks that have them
- Make a listener that isn't using the dev webserver
- write instructions on how to run/stop at startup/shutdown systemd
- Pretty the notifications (ie add image, etc)
- Make python2.7 backwards compatible (future use with aws lambda)
- Fix all the things =)