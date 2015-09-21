from nebriosmodels import NebriOSModel, NebriOSField


class Order(NebriOSModel):
    date_placed = NebriOSField(required=True, default=datetime.now)
    menu_item = NebriOSField(required=True)

    def get_name(self):
        if self.menu_item == 1:
            return 'PB&J on white'
        elif self.menu_item == 1:
            return 'PB&J on wheat'
        elif self.menu_item == 1:
            return 'Turkey on white'
        elif self.menu_item == 1:
            return 'Turkey on wheat'
