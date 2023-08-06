import requests

def RequestsPool (pool_facor = 10):
    s = requests.Session ()
    s.mount(
        'https://',
        requests.adapters.HTTPAdapter (pool_connections = pool_facor, pool_maxsize = pool_facor)
    )
    s.mount(
        'http://',
        requests.adapters.HTTPAdapter (pool_connections = pool_facor, pool_maxsize = pool_facor)
    )
    return s


if __name__ == "__main__":
    p = Pool (10)
    print (p.get ("http://example.com"))
    print (p.get ("http://example.com"))
