

def construct_unique_key(baseurl, params):
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

endpoint_url = 'https://api.twitter.com/1.1/search/tweets.json'
params = {'q': '@umsi', 'count':'100', 'lang': 'en'}
print(construct_unique_key(endpoint_url, params))

