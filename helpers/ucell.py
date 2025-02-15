import requests
import pickle


# from func.logger import logging


class Ucell:

    def __init__(self, phone):
        self.__headers = {
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uz;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://my.ucell.uz",
            "Referer": "https://my.ucell.uz/Account/Login",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
        }
        self.__login_url = "https://my.ucell.uz/Account/Login"
        self.__send_message_url = "https://my.ucell.uz/PcSms/SendSms"
        self.__send_otp_url = "https://my.ucell.uz/Account/GetOtpBySms"
        self.__set_password_url = "https://my.ucell.uz/Account/SetPwd"
        self.__password = "MyUcellParol08"
        self.__phone = phone
        try:
            with open(f"sessions/{self.__phone}.db", "rb") as file:
                self.__cookies = pickle.load(file)
        except:
            self.__cookies = []
        self.__otp_headers = {
            "accept": "*/*",
            "accept-language": "uz,en;q=0.9,ru;q=0.8",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Yandex";v="23"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "cookie": "_ga=GA1.2.252888730.1670757045; ht=691a0395e6826dcc085fa307e73b4db2f903191c%7Emob; lang=b4820c68a2a4a7314de9e0226dca83c37b61a3a4%7Euz; mpg=0a40870dd4a1502dcd7a9213f6c2b56c9b8a6694%7E1; fs=24f07c656b7ce581d387060cf26f0df3587412cf%7E1680024279; _gid=GA1.2.1664522425.1680024316; _crp=s; .UWCCFRONTNXAUTH=BB88D6AEFBCE9DE2B18E0763B0DED38F745515241F2D693583CBF67360E3F57555A157CB1CB70128E6536EFB10CA27DD443545C0EF9D85240B175049655825925EFE9202608E7C484AB3E3CB7D6F1634C3E95FFC258DDA97E3789DB20F86E4633821A6D096528B20977058D7235628D1D1ECDE27B7DAD3E8DEE75B5E20985E9A17AD58C5433B50EE2B273A7AF7BC6217C0527C3B58E54307EF4B63975DE69FDA831B657CAC06E1C4B5D8D741AB5A5AC69EB4596039588532F687D3B5A96661FEF5B15439E96763BE1103BD064B679528B481872B532DCBB838FD807AD0E66A71DE3D70BE158EEACC14F3BD366C2509EC31B8E9ABBC101721D86F66E4BEA99FDC2F7288B5CA2B555756A372B87317720DFAE1DE8561EC1C97E9B08A88D8D3CDAFE0710D4A99617D6CA38980BE449E48568401F8AEED973F34D296F2A44ADB806BEB53D886E7036D1B25F7B092CB811F29; ASP.NET_SessionId=og1zketqtbeq2tflcab12m5w; _culture=uz; _gat=1",
            "Referer": "https://my.ucell.uz/Account/Login?ReturnUrl=%2f",
            "Referrer-Policy": "no-referrer-when-downgrade",
        }

    def login(self, password="", otp="", login_type=1):
        data = {
            "phone_number": self.__phone,
            "password": password,
            "ot_password": otp,
            "pin": "null",
            "login_type": f"{login_type}",
            "return_url": "/",
        }
        try:
            res = requests.post(
                url=self.__login_url, headers=self.__headers, data=data
            )
            data = res.json()
            if data["success"] == True:
                with open(f"sessions/{self.__phone}.db", "wb") as file:
                    pickle.dump(res.cookies, file)
                    return True
            else:
                return {"response": "otp.not.confirmed"}
        except Exception as e:
            print(e)
            return {"response": "server.error"}

    def sendMessage(self, to_phone, message, i=0):
        data = {
            "msisdn": str(to_phone),
            "text": str(message),
            "date": "null",
        }
        try:

            res = requests.post(
                url=self.__send_message_url,
                headers=self.__headers,
                data=data,
                cookies=self.__cookies,
            ).json()
            return res
        except Exception as e:
            if i == 0:
                res = self.login(password=self.__password, login_type="3")
                try:
                    with open(f"sessions/{self.__phone}.db", "rb") as file:
                        self.__cookies = pickle.load(file)
                except:
                    self.__cookies = []
                return self.sendMessage(to_phone, message, i=1)
            return {"response": "server.error"}

    def sendOtp(self):
        data = {
            "phone": self.__phone,
        }
        try:
            res = requests.post(
                url=self.__send_otp_url, headers=self.__otp_headers, data=data
            ).json()
            return res
        except:
            return {"response": "server.error"}

    def setPassword(self, password=None, otp=None):
        if password == None:
            password = self.__password
        data = {
            "phone": self.__phone,
            "password": password,
            "otp": otp,
            "mode": 1,
            "confirmed": 1,
        }
        try:
            res = requests.post(
                url=self.__set_password_url, headers=self.__headers, data=data
            ).json()
            return res
        except:
            return {"response": "server.error"}


Ucell = Ucell("998940105669")
#
# res = Ucell.login(password="Samandar001@",login_type=3)
# res = Ucell.sendMessage("998943990509", "ishladiku")
# Ucell.sendOtp()
# Ucell.setPassword("Samandar001@","667717")
# print(res)
