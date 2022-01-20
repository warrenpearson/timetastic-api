import json
import os
import sys

import requests


class User:
    def __init__(self, user_id, name, approver_id):
        self.user_id = user_id
        self.name = name
        self.approver_id = approver_id


class Timetastic:
    def get_users(self):
        url = "http://app.timetastic.co.uk/api/users"
        token = os.environ["TT_TOKEN"]

        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

        if response.status_code != 200:
            print(f"Request GET {url} failed with code {response.status_code}")
            sys.exit(1)

        data = json.loads(response.text)

        users = dict()
        names = []
        approver_list = set()

        for person in data:
            user_id = person["id"]
            approver_id = person["approverId"]
            approver_list.add(approver_id)
            users[user_id] = User(
                person["id"],
                f'{person["firstname"]} {person["surname"]}',
                approver_id,
            )

        for user_id in users.keys():
            user = users[user_id]
            approver_id = user.approver_id
            # name = f"{user.name} [{user.user_id}]"
            name = user.name
            if approver_id != 0:
                approver = users[approver_id].name
                name += f": {approver}"
            names.append(name)

        return sorted(names)


if __name__ == "__main__":
    user_names = Timetastic().get_users()
    for n in user_names:
        print(n)
