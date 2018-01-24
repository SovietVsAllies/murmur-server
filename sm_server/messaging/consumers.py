import json
from urllib.parse import parse_qs

from channels import Channel
from channels.sessions import channel_session
from django.core.exceptions import ObjectDoesNotExist

from account.models import Account
from messaging.models import ActiveChannel
from messaging.models import PendingMessage


@channel_session
def message_connect(message):
    message.reply_channel.send({'accept': True})
    params = parse_qs(message.content['query_string'])
    if b'user' in params:
        try:
            user = params[b'user'][0].decode('utf-8')
            message.channel_session['user'] = user
            owner = Account.objects.get(id=user)
            channel = ActiveChannel.objects.filter(owner=owner)
            if channel.exists():
                channel.delete()
            channel = ActiveChannel(owner=owner, name=message.reply_channel.name)
            channel.save()
            return
        except ObjectDoesNotExist:
            pass
    message.reply_channel.send({'close': True})


@channel_session
def message_consumer(message):
    try:
        content = message.content['text']
        data = json.loads(content)
        receiver = Account.objects.get(id=data['receiver'])
        channel = ActiveChannel.objects.filter(owner=receiver)
        if channel.exists():
            channel = Channel(channel.get().name)
            channel.send({
                'text': message.channel_session['user'] + ': ' + data['content'],
            })
        else:
            PendingMessage(receiver=receiver, payload=data['content'].encode('utf-8')).save()
    except ObjectDoesNotExist:
        pass


@channel_session
def message_disconnect(message):
    owner = Account.objects.get(id=message.channel_session['user'])
    ActiveChannel.objects.get(owner=owner).delete()
