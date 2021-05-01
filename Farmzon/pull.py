import requests
import json
from pusher_push_notifications import PushNotifications


beams_client = PushNotifications(
    instance_id='4eacff80-61d8-48d7-ba72-9e7aede4119c',
    secret_key='4A9C78664B4FCC25397DD2F780028D9967F69BA4229736B49420727081646EFC',
)
response = beams_client.publish_to_interests(
  interests=['hello'],
  publish_body={
    'apns': {
      'aps': {
        'alert': {
          'title': 'Hello',
          'body': 'Hello, world!',
        },
      },
    },
    'fcm': {
      'notification': {
        'title': 'Hello',
        'body': 'Hello, world!',
      },
    },
    'web': {
      'notification': {
        'title': 'Hello',
        'body': 'Hello, world!',
      },
    },
  },
)

print(response['publishId'])