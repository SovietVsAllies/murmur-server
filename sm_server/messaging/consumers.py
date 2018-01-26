import base64
import json
import traceback
import uuid
from urllib.parse import parse_qs

from channels import Channel
from channels.sessions import channel_session

from account.models import Account
from messaging.models import ActiveChannel
from messaging.models import PendingMessage


@channel_session
def message_connect(message):
    message.reply_channel.send({'accept': True})
    params = parse_qs(message.content['query_string'])
    try:
        owner = params[b'account_id'][0].decode() + '=='
        message.channel_session['owner'] = owner
        owner = uuid.UUID(bytes=base64.b64decode(owner))
        owner = Account.objects.get(id=owner)
        channel = ActiveChannel.objects.filter(owner=owner)
        if channel.exists():
            channel.delete()
        channel = ActiveChannel(owner=owner, name=message.reply_channel.name)
        channel.save()
        return
    except:
        traceback.print_exc()
    message.reply_channel.send({'close': True})


@channel_session
def message_consumer(message):
    try:
        content = message.content['text']
        data = json.loads(content)
        if data['type'] == 'send_message':
            data = data['data']
            receiver = uuid.UUID(bytes=base64.b64decode(data['receiver'] + '=='))
            receiver = Account.objects.get(id=receiver)
            channel = ActiveChannel.objects.filter(owner=receiver)
            if channel.exists():
                channel = Channel(channel.get().name)
                channel.send({'text': json.dumps({
                    'type': 'received_message',
                    'data': {
                        'sender': message.channel_session['owner'],
                        'content': data['content'],
                    },
                })})
            else:
                PendingMessage(receiver=receiver, payload=data['content'].encode()).save()
    except:
        traceback.print_exc()


@channel_session
def message_disconnect(message):
    owner = message.channel_session['owner'] + '=='
    owner = Account.objects.get(id=uuid.UUID(bytes=base64.b64decode(owner)))
    ActiveChannel.objects.get(owner=owner).delete()
