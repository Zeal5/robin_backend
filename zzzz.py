import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time





def main():
    urls = "http://127.0.0.1:8000/1234/secret/address"

    response = requests.get(urls)
    print(response.text)
    print(response.status_code)





if __name__ == "__main__":
    main()




