import requests
import time
import datetime

class ZalandoNewsletter:
    def __init__(self, proxies=None):
        self.session = requests.session()
        self.session.proxies = proxies

    def generate_code(self, region="pl", save_to_file=False) -> str:
        self.region = region

        self.email = self.get_email()
        self.verify_status = self.send_request()
        if self.verify_status:
            self.verify_email()
        
        self.code = self.get_code()
        print(self.code)
        if save_to_file:
            self.save_code()

        return self.code

    def get_email(self) -> str:
        url = "https://api.internal.temp-mail.io/api/v3/email/new"
        headers = {'user-agent': 'vscode-restclient'}
        response = self.session.post(url, headers=headers).json()
        return response["email"]

    def send_request(self) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Content-Type': 'application/json',
        }
        payload = {
            "id": "06fe5b50b4218612aa3fa8494df326aef7ff35a75a8563b3455bb53c15168872",
            "variables": {
            "input": {
                "email": self.email,
                "preference": {
                    "category": "MEN",
                    "topics": [
                        {
                            "id": "item_alerts",
                            "isEnabled": True
                        },
                        {
                            "id": "survey",
                            "isEnabled": True
                        },
                        {
                            "id": "recommendations",
                            "isEnabled": True
                        },
                        {
                            "id": "fashion_fix",
                            "isEnabled": True
                        },
                        {
                            "id": "follow_brand",
                            "isEnabled": True
                        },
                        {
                            "id": "subscription_confirmations",
                            "isEnabled": True
                        },
                        {
                            "id": "offers_sales",
                            "isEnabled": True
                        }
                    ]
                },
                "referrer": "nl_subscription_banner_one_click",
                "clientMutationId": "1620930739401"
            }
            }
        }

        url = f"https://www.zalando.{self.region}/api/graphql/"
        response = self.session.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            if response.json()["data"]['subscribeToNewsletter']['isEmailVerificationRequired'] == False:
                return False
            else:
                return True
        else:
            raise Exception(f"Status code: {response.status_code}")

    def verify_email(self) -> None:
        while True:
            url = f"https://api.internal.temp-mail.io/api/v3/email/{self.email}/messages"
            headers = {'user-agent': 'vscode-restclient'}

            response = self.session.get(url, headers=headers)
            print(response.json())
            if response.status_code == 200 and len(response.json()) > 0:
                message = response.json()[0]
                verify_args = message["body_text"].split("confirmation?")[1].split(">")[0]
                print(verify_args)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                    'Content-Type': 'application/json',
                }
                url = f"https://www.zalando.{self.region}/zalando-newsletter/confirmation?{verify_args}"
                response = self.session.get(url, headers=headers)
                if response.status_code == 200:
                    return
            
            time.sleep(3)

    def get_code(self) -> str:
        found_message = False
        while found_message == False:
            url = f"https://api.internal.temp-mail.io/api/v3/email/{self.email}/messages"
            headers = {'user-agent': 'vscode-restclient'}

            response = self.session.get(url, headers=headers)
            if self.verify_status:
                if response.status_code == 200 and len(response.json()) > 1:
                    message = response.json()[1]
                    found_message = True
            else:
                if response.status_code == 200 and len(response.json()) > 0:
                    message = response.json()[0]
                    found_message = True

        code = message["body_text"].split('[→]')[0].split('\n')[len(message["body_text"].split('[→]')[0].split('\n')) - 1].replace(' ', '').replace('\n', '')
        return code

    def save_code(self) -> None:
        filename = f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {self.region}.txt"
        with open(filename, "w+") as file:
            file.write(self.code)
        return

