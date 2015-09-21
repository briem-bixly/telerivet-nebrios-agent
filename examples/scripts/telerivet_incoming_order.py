from sandwhichshopmodels import Order

from telerivetutils import respond_to_message, error_response


class telerivet_incoming_response(NebriOS):
    listens_to = ['sms_body']

    def check(self):
        return 'order' in self.sms_body and \
               self.handled is False and \
               self.sms_direction == 'incoming'

    def action(self):
        try:
            sandwich_num = self.sms_body.split(' ')[1]
            if type(sandwich_num) != int:
                response = error_response(self,
                                          """
                                          Sorry, we didn't quite get that. Please try again. i.e. order 2.
                                          """, close_convo=True)
            else:
                order = Order(
                    menu_item=sandwich_num
                )
                order.save()
                message = "Thank you for ordering %s. Your order number is %s." %(order.get_name(), order.PROCESS_ID)
                response = respond_to_message(self, message, close_convo=True)
            self.date_handled = datetime.now()
            self.handled = True
        except:
            # we got an error somewhere... this will get picked up in retry_send
            pass