from nebriosmodels import NebriOSModel, NebriOSField, NebriOSReference


class Conversation(NebriOSModel):
    date_started = NebriOSField(required=True, default=datetime.now)
    external_number = NebriOSField(required=True)
    telerivet_number = NebriOSField()
    is_active = NebriOSField(required=True, default=False)

    def get_messages(self):
        return Message.filter(conversation=self)


class Message(NebriOSModel):
    date_received = NebriOSField(required=True, default=datetime.now)
    telerivet_id = NebriOSField(required=True, default='')
    sms_to = NebriOSField(required=True)
    sms_from = NebriOSField(required=True)
    sms_body = NebriOSField(required=True)
    sms_status = NebriOSField(required=True, default='')
    sms_direction = NebriOSField(required=True, default='')
    sent = NebriOSField(required=True, default=False)
    date_sent = NebriOSField()
    handled = NebriOSField(required=True, default=False)
    date_handled = NebriOSField()
    raw_data = NebriOSField(required=True, default='')
    conversation = NebriOSReference(Conversation, required=True)


class Project(NebriOSModel):
    project_id = NebriOSField(required=True)
    api_key = NebriOSField(required=True)