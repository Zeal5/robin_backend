from dataclasses import dataclass
from pydantic import BaseModel


# @dataclass
# class TokenBalance:
#     balance : float
#     symbol : str | None = None

# class A(BaseModel):
#     balance : float
#     symbol : str | None = None

# a = A(**{'balance':123,'symbol':"ART"})
# b = TokenBalance(**{'balance':123,'symbol':"ART"})
# print(a.symbol)
# print(b.symbol)

"""
          *
         * *
        * * * 
         * *
          *
"""

# reverse = False
# x = 0

# for i in range(1, e := int(input("enter number :"))):
#     if i == e // 2:
#         reverse = True
#     if not reverse:
#         print(f"{'* ' * i:^{int(e) * 2}}")
#     else:
#         print(f"{'* ' * (i-x):^{int(e)*2}}")
#         x += 2


import requests
import threading

def main(i):
    print(f"sending {i} request...")
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
}
    r = requests.get("https://zaksteryt.w3spaces.com/",headers=headers)
    print(f"status for request {i} => {r}")
    print(r.headers)

threads = []
for i in range(10000):
    a = threading.Thread(target = main,args=(i,))
    a.start()
    threads.append(a)

for i in threads:
    i.join()


