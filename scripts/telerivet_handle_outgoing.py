from telerivetmodels import Message
from telerivetutils import send_new_message


class telerivet_handle_outgoing(NebriOS):
    listens_to = ['sms_to', 'sms_body']

    def check(self):
        return self.sms_to != '' and \
               self.sms_body != '' and \
               self.sent is False

    def action(self):
        # do things with the outgoing message
        try:
            new_msg = send_new_message(self.sms_to, self.sms_body)
        except:
            # something happened and we got an error... do nothing with this message.
            pass