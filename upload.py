import asyncio
import requests
from pprint import pprint


WEBSITES = {'url':'https://sm.ms',
            'doc':'https://sm.ms/doc/',
            'api':'https://sm.ms/api/upload',
            'params':{'ssl':True, 'format':'json'},
            'files':'smfile'}


def uploadImage(path):
    with open(path, 'rb') as f:
        req = requests.post('https://sm.ms/api/upload', params={'ssl':True, 'format':'json'}, files={'smfile':f})
        res = req.json()
    return res


# coroutine
def uploadImages(paths):
    async def uploadImage(path):
        with open(path, 'rb') as f:
            req = requests.post('https://sm.ms/api/upload', params={'ssl':True, 'format':'json'}, files={'smfile':f})
            res = req.json()
            results[path] = res
    results = {}
    coroutines = [uploadImage(path) for path in paths]
    eventLoop = asyncio.get_event_loop()
    try:
        eventLoop.run_until_complete(asyncio.wait(coroutines))
    finally:
        eventLoop.close()
    return results


if __name__ == '__main__':
    # a = uploadImage('1.jpg')
    # pprint(a)
    b = uploadImages([r'1.jpg', r'2.png'])
    pprint(b)
