from telerivetmodels import Message
from telerivetutils import respond_to_message


class telerivet_handle_incoming(NebriOS):
    listens_to = ['raw_data']

    def check(self):
        return self.raw_data != '' and self.handled == False

    def action(self):
        # Do stuff with incoming message
        if self.status == 'not_delivered' or self.status == 'failed':
            # check raw_data for more info
            error_msg = self.raw_data['error_message']
            # handle based on error
        if self.direction == 'incoming':  # need to add to this check to respond with appropriate message
            response = respond_to_message(self, 'appropriate message')

        self.date_handled = datetime.now()
        self.handled = True