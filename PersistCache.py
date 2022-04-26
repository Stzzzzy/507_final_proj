import datetime
import json

CACHE_FILENAME = "cache.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def fib(n):
    fib_seq = [0, 1]
    for i in range(2, n):
        fib_seq.append(fib_seq[i - 2] + fib_seq[i - 1])
    return fib_seq[-1]


def fib_with_cache(n):
    n_key = str(n)
    if n_key in FIB_CACHE:
        return FIB_CACHE[n_key]
    else:
        FIB_CACHE[n_key] = fib(n)
        save_cache(FIB_CACHE)
        return FIB_CACHE[n_key]
    
FIB_CACHE = open_cache()

inp = input("What Fibonacci number would you like? ")
t1 = datetime.datetime.now().timestamp()
print(fib_with_cache(int(inp)))
t2 = datetime.datetime.now().timestamp()

inp = input("What Fibonacci number would you like? ")
t3 = datetime.datetime.now().timestamp()
print(fib_with_cache(int(inp)))
t4 = datetime.datetime.now().timestamp()

print("time without caching: ", (t2 - t1) * 1000, "ms")
print("time with caching: ", (t4 - t3) * 1000, "ms")