from nebrios_authentication import token_required
from telerivetmodels import Message, Conversation
import logging


@token_required(realm='telerivet')
def incoming_message(request):
    data = request.POST
    if data['secret'] != 'ZFG4P3KLHTRLXT4DPFAZWC6QUMMKANX9':
        return HttpResponseForbidden
    try:
        msg = Message.get(telerivet_id=data['id'])
        # we've already received this message. return 200 ok
        return {}
    except Process.DoesNotExist:
        msg = Message(
            telerivet_id=data['id'],
            sms_to=data['to_number'],
            sms_from=data['from_number'],
            sms_body=data['content'],
            sms_status=data['status'],
            sms_direction=data['direction'],
            raw_data=data
        )
    try:
        convo = Conversation.get(external_number=data['from_number'], is_active=True)
        if convo.telerivet_number != data['to_number']:
            convo.telerivet_number = data['to_number']
    except Process.DoesNotExist:
        convo = Conversation(
            external_number=data['from_number'],
            telerivet_number=data['to_number'],
            is_active=True
        )
    convo.save()

    msg.conversation = convo
    msg.save()


@token_required(realm='telerivet')
def outgoing_message(request):
    data = request.POST
    if data['secret'] != 'BTOIJaktfp6SopAQBQdGXFE7vBPPlM':
        return HttpResponseForbidden
    try:
        msg = Message.get(telerivet_id=data['id'])
        # we sent this message. let's update.
        # only a destination number and content are required to send a message
        msg.sms_from = data['from_number']
        msg.sms_status = data['status']
        msg.sms_direction = data['direction']
        msg.raw_data = data
    except Process.DoesNotExist:
        # this outgoing message wasn't sent via our api.
        # create new
        msg = Message(
            telerivet_id=data['id'],
            sms_to=data['to_number'],
            sms_from=data['from_number'],
            sms_body=data['content'],
            sms_status=data['status'],
            sms_direction=data['direction'],
            sent=True,
            date_sent=data['time_created'],
            raw_data=data
        )
    try:
        convo = Conversation.get(external_number=data['from_number'], is_active=True)
        if convo.telerivet_number != data['to_number']:
            convo.telerivet_number = data['to_number']
    except Process.DoesNotExist:
        convo = Conversation(
            external_number=data['from_number'],
            telerivet_number=data['to_number'],
            is_active=True
        )
    convo.save()

    msg.conversation = convo
    msg.save()


def generate_outgoing_message(to, content):
    message = Message()
    message.sms_to = to
    message.sms_body = content
    message.save()