from telerivetmodels import Message, Conversation, Project
import requests


def send_new_message(to, content):
    try:
        convo = Conversation.get(external_number=to)
    except Process.DoesNotExist:
        convo = Conversation(
            external_number=to,
            is_active=True
        )
        convo.save()
    msg = Message(
        sms_to=to,
        sms_body=content,
        conversation=convo
    )
    msg.save()
    return send_msg(msg)


def respond_to_message(message, content, close_convo=False):
    convo = message.conversation
    if close_convo:
        convo.is_active = False
        convo.save()
    msg = Message(
        sms_to=message.sms_from,
        sms_body=content,
        conversation=convo
    )
    msg.save()
    return send_msg(msg)


def send_msg(message):
    keys = Project.filter()[0]
    if keys.length == 0:
        return {'msg': 'Error: API key and project id must be set up before sending messages', 'status': 'failed'}
    try:
        new_msg = requests.post(
            'https://api.telerivet.com/v1/projects/%s/messages/send' % keys.project_id,
            auth=(keys.api_key, ''),
            data={'to_number': message.sms_to, 'content': message.sms_body}
        )
        message.telerivet_id = new_msg['id']
        message.sent = True
        message.date_sent = datetime.now()
        message.save()
        return {'msg': 'Message sent and created', 'status': 'success'}
    except Exception, e:
        return {'msg': str(e), 'status': 'failed'}