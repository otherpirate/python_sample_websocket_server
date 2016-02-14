import random

from autobahn.twisted.websocket import WebSocketServerFactory

from user import User

class Factory(WebSocketServerFactory):

    def __init__(self, *args, **kwargs):
        super(Factory, self).__init__(*args, **kwargs)
        self.users = {}

    def register(self, client):
        new_user = User(client, None)
        self.users[client.peer] = new_user
        new_user.client.sendMessage("Welcome!")

    def unregister(self, client):
        user = self.users[client.peer]
        if user.partner:
            user.partner.client.sendMessage("Server lose connection with your partner %s" % user)
        self.users.pop(client.peer)

    def findPartner(self, client):
        available_partners = self.get_users_without_partners(client)

        if not available_partners:
            client.sendMessage("No partners for %s, waiting for a partner..." % str(client.peer))
        else:
            # Take a random partner
            partner_key = random.choice(available_partners)
            self.users[partner_key].partner = self.users[client.peer]
            self.users[client.peer].partner = self.users[partner_key]

            client.sendMessage("Your partner is %s" % self.users[client.peer].partner)
            self.users[partner_key].client.sendMessage("Your partner is %s" % self.users[partner_key].partner)

    def communicate(self, client, payload, isBinary):
        user = self.users[client.peer]
        user.client.sendMessage("Server received: %s" % payload)

        if user.partner:
            client.sendMessage("Sending to %s" % user.partner)
        else:
            client.sendMessage("You don't have partner")

    def get_users_without_partners(self, client):
        return [user for user in self.users
                if user != client.peer and not self.users[user].partner]