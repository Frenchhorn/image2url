'''
https://docs.python.org/3/library/concurrent.futures.html
'''

import time
import shutil
import requests
import math
import concurrent.futures
from concurrent.futures import Executor, ThreadPoolExecutor, ProcessPoolExecutor


def sample_test():
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(pow, 2, 323)
        print(future.running())
        print(future.done())
        # future.add_done_callback((lambda x : x*2)(123))
        print(future.result())


def copy_test():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(shutil.copy, '1.jpg', '1_copy.jpg')
        executor.submit(shutil.copy, '2.png', '2_copy.png')


def dead_lock_test():
    def wait_on_b():
        time.sleep(2)
        print(b.result(timeout=10))  # b will never complete because it is waiting on a.
        return 5

    def wait_on_a():
        time.sleep(3)
        print(a.result())  # a will never complete because it is waiting on b.
        return 6

    executor = ThreadPoolExecutor(max_workers=2)
    a = executor.submit(wait_on_b)
    b = executor.submit(wait_on_a)


def dead_lock_2_test():
    def wait_on_future():
        f = executor.submit(pow, 5, 2)
        # This will never complete because there is only one worker thread and
        # it is executing this function.
        print(f.result())

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(wait_on_future)


def thread_pool_executor_test():
    urls = ['https://www.foxnews.com/',
            'https://www.baidu.com',
            'https://www.bing.com',
            'https://www.python.org/']

    def load_url(url, timeout):
        req = requests.get(url, timeout=timeout)
        return req.content

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(load_url, url, 10) : url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))


def process_pool_executor_test():
    # ERROR
    PRIMES = [
        112272535095293,
        112582705942171,
        112272535095293,
        115280095190773,
        115797848077099,
        1099726899285419]

    def is_prime(n):
        if n % 2 == 0:
            return False

        sqrt_n = int(math.floor(math.sqrt(n)))
        for i in range(3, sqrt_n + 1, 2):
            if n % i == 0:
                return False
        return True

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    sample_test()
    # copy_test()
    # dead_lock_test()
    # thread_pool_executor_test()
    # process_pool_executor_test()