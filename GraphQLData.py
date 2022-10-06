import ujson


def getHeader(queryName):
    apiFiles = open("Files/APICalls.json")
    key = ujson.loads(apiFiles.read())[queryName]
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://opensea.io",
        "Referer": "https://opensea.io/",
        "Authority": "api.opensea.io",
        "sec-fetch-mode": "cors",
        "x-signed-query": key
    }
    apiFiles.close()
    return header


def getQuery(queryName, **variables):
    queryBodies = open("Files/QueryBodies.json")
    body = ujson.loads(queryBodies.read())[queryName]
    request = {
        "id": queryName,
        "query": body,
        "variables": variables
    }
    queryBodies.close()
    return ujson.dumps(request)
