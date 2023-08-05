import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import time

def send_request(url, request_number):
    try:
        response = requests.get(f"{url}/{request_number}")
        print(f"Request {request_number}: Status code for {url}: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request {request_number}: Error occurred while sending request to {url}: {e}")


def main():
    urls = ["http://localhost:8000"] * 10000  # Replace with your server URL

    start_time = time.time()

    # Use ThreadPoolExecutor to send requests concurrently
    with ThreadPoolExecutor(max_workers=1000) as executor:
        for i, url in enumerate(urls, start=1):
            executor.submit(send_request, url, i)

    end_time = time.time()

    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()




