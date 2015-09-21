from sandwichshopmodels import Order

from telerivetutils import respond_to_message


class telerivet_incoming_menu(NebriOS):
    listens_to = ['sms_body']

    def check(self):
        return self.sms_body == 'menu' and \
               self.handled is False and \
               self.sms_direction == 'incoming'

    def action(self):
        try:
            response = respond_to_message(self,
                                          """
                                          [1] PB&J on white
                                          [2] PB&J on wheat
                                          [3] Turkey on white
                                          [4] Turkey on wheat
                                          """, close_convo=True)
            self.date_handled = datetime.now()
            self.handled = True
        except:
            # we got an error somewhere... this will get picked up in retry_send
            pass