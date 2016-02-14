class User:
    def __init__(self, client, partner):
        self.client = client
        self.partner = partner

    def send_message(self, message):
        self.client.sendMessage(str(message))

    def send_message_to_partner(self, message):
        self.partner.send_message(str(message))

    def __str__(self):
        return str(self.client.peer)
