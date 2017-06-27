import requests
import concurrent.futures
from pprint import pprint


WEBSITES = {'url':'https://sm.ms',
            'doc':'https://sm.ms/doc/',
            'api':'https://sm.ms/api/upload',
            'params':{'ssl':True, 'format':'json'},
            'files':'smfile'}
results = {}
errors = {}


def uploadImage(path):
    with open(path, 'rb') as f:
        req = requests.post('https://sm.ms/api/upload', params={'ssl':True, 'format':'json'}, files={'smfile':f}, verify=True)
        res = req.json()
    return res


# ThreadPool
def uploadImages(paths):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_to_path = {executor.submit(uploadImage, path) : path for path in paths}
        for future in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[future]
            try:
                results[path] = future.result()
                print('[SUCCESS] %s'%(path))
            except Exception as exc:
                errors[path] = str(exc)
                print('[ERROR]%s : %s'%(path, exc))


if __name__ == '__main__':
    uploadImages([r'pics/1.jpg', r'pics/2.png', r'pics/3.png', r'pics/4.jpg', r'pics/5.jpg', r'pics/6.jpg'])
    pprint(results)
    pprint(errors)