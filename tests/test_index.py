import requests
import time

# Make sure the index page returns 200 for all supported http methods
def test_index_http_methods():
    assert requests.request('GET', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('HEAD', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('POST', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('PUT', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('DELETE', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('CONNECT', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('OPTIONS', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('TRACE', 'http://localhost:5000').status_code == 200
    time.sleep(0.1)
    assert requests.request('PATCH', 'http://localhost:5000').status_code == 200