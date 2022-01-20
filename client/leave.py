import datetime
import json
import os
import sys

import requests


class Leave:
    def for_user(self, user):
        url = "http://app.timetastic.co.uk/api/users/" + user
        token = os.environ["TT_TOKEN"]

        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

        if response.status_code != 200:
            print(f"Request GET {url} failed with code {response.status_code}")
            sys.exit(1)

        data = json.loads(response.text)
        years = data["allowances"]
        data = None
        this_year = datetime.date.today().year

        for year in years:
            if year["year"] == this_year:
                data = year
                break

        data = f'{data["year"]}: {data["allowance"]} / {data["remaining"]}'
        return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 leave.py <user_id> ie 372574")
        sys.exit()
    user = sys.argv[1]
    user_details = Leave().for_user(user)
    print(user_details)
