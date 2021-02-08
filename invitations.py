class Friend:
    def __init__(self, name):
        self.name = name
        self.message = 'No party...'

    def invite(self, message):
        self.message = message

    def show_invites(self):
        return self.message


class Party:
    def __init__(self, party):
        self.party = party
        self.friends = []

    def add_friend(self, name):
        self.friends.append(name)

    def del_friend(self, name):
        self.friends.remove(name)

    def send_invites(self, date):
        for friend in self.friends:
            friend.invite(f'{self.party}: {date}')
