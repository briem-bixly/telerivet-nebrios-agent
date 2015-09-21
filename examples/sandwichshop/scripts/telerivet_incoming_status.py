from sandwichshopmodels import Order

from telerivetutils import respond_to_message, error_response


class telerivet_incoming_status(NebriOS):
    listens_to = ['sms_body']

    def check(self):
        return 'order' in self.sms_body and \
               self.handled is False and \
               self.sms_direction == 'incoming'

    def action(self):
        try:
            order_id = self.sms_body.split(' ')[1]
            if type(order_id) != int:
                response = error_response(self,
                                          """
                                          Sorry, we didn't quite get that. Please try again. i.e. status 2.
                                          """, close_convo=True)
            else:
                order = Order.get(PROCESS_ID=order_id)
                time_since_order = datetime.now() - order.date_placed
                if time_since_order.seconds / 60 > 10:
                    message = "Order %s has been picked up." % order.PROCESS_ID
                elif time_since_order.seconds / 60 > 5:
                    message = "Order %s is ready for pick up." % order.PROCESS_ID
                response = respond_to_message(self, message, close_convo=True)
            self.date_handled = datetime.now()
            self.handled = True
        except:
            # we got an error somewhere... this will get picked up in retry_send
            pass