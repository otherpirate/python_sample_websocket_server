class User:
    def __init__(self, client, partner):
        self.client = client
        self.partner = partner

    def __str__(self):
        return str(self.client.peer)
