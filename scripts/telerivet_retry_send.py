from telerivetmodels import Message, Project
from telerivetutils import send_new_message


class telerivet_retry_send(NebriOS):
    listens_to = ['telerivet_retry_send']

    def check(self):
        project = Project.filter()[0]
        return project.length > 0 and \
               project.api_key != '' and \
               project.project_id != ''

    def action(self):
        pending_messages = Message.filter(sent=False, sms_direction='')
        for message in pending_messages:
            try:
                new_msg = send_new_message(message.sms_to, message.sms_body)
            except:
                # something happened and we got an error... do nothing with this message.
                pass
