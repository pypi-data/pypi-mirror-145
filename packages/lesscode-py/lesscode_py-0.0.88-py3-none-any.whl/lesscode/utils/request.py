import json
import aiohttp
import tornado.options
import requests
import py_eureka_client.eureka_client as eureka_client


async def post(path, data=None,
               base_url=tornado.options.options.data_server,
               result_type="json", pack=True, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(base_url + path, json=data, **kwargs) as resp:
            if result_type == "json":
                result = await resp.json()
                if not pack:
                    result = result.get("data")
            elif result_type == "text":
                result = await resp.text()
            else:
                result = await resp.content
            return result


async def get(path, params=None, base_url=tornado.options.options.data_server, result_type="json", pack=True, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + path, params=params, **kwargs) as resp:
            if result_type == "json":
                result = await resp.json()
                if not pack:
                    result = result.get("data")
            elif result_type == "text":
                result = await resp.text()
            else:
                result = await resp.content
            return result


def sync_get(path, params=None, base_url=tornado.options.options.data_server, result_type="json", pack=True, **kwargs):
    res = requests.get(base_url + path, params=params, **kwargs)
    if result_type == "json":
        res = res.json()
        if not pack:
            res = res.get("data")
    elif result_type == "text":
        res = res.text
    else:
        res = res.content
    return res


def sync_post(path, data=None,
              base_url=tornado.options.options.data_server,
              result_type="json", pack=True, **kwargs):
    res = requests.post(base_url + path, json=data, **kwargs)
    if result_type == "json":
        res = res.json()
        if not pack:
            res = res.get("data")
    elif result_type == "text":
        res = res.text
    else:
        res = res.content
    return res


def eureka_request(path="", return_type="json", method="GET", data=None, app_name="DATA_SERVICE", pack=True, **kwargs):
    if not kwargs.get("headers"):
        kwargs.update({"headers": {
            "Content-Type": "application/json"
        }})
    res = eureka_client.do_service(app_name=app_name, service=path, return_type=return_type, method=method, data=data,
                                   **kwargs)
    if return_type == "json" and not pack:
        res = res.get("data")
    return res


def eureka_get(path="", return_type="json", data=None, app_name="DATA_SERVICE", pack=True, **kwargs):
    res = eureka_request(path=path, return_type=return_type, method="GET", data=data, app_name=app_name, pack=pack,
                         **kwargs)
    return res


def eureka_post(path="", return_type="json", data=None, app_name="DATA_SERVICE", pack=True, **kwargs):
    res = eureka_request(path=path, return_type=return_type, method="POST", data=json.dumps(data), app_name=app_name,
                         pack=pack, **kwargs)
    return res
