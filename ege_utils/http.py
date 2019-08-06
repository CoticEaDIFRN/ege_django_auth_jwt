"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from django.conf import settings
from http.client import HTTPException
import requests
import json

default_headers = {"Authorization": "Secret %s" % settings.EGE_ACESSO_JWT_SECRET}


def get(url, headers={}, encoding='utf-8', decode=True, **kwargs):
    response = requests.get(url, headers=headers.update(default_headers), **kwargs)

    if response.ok:
        byte_array_content = response.content
        return byte_array_content.decode(encoding) if decode and encoding is not None else byte_array_content
    else:
        exc = HTTPException('%s - %s' % (response.status_code, response.reason))
        exc.status = response.status_code
        exc.reason = response.reason
        exc.headers = response.headers
        exc.url = url
        raise exc


def get_json(url, headers={}, encoding='utf-8', json_kwargs={}, **kwargs):
    content = get(url, headers=headers, encoding=encoding, **kwargs)
    return json.loads(content, **json_kwargs)


def post(url, data=None, json_data=None, headers={}, encoding='utf-8', decode=True, **kwargs):
    response = requests.post(url, data, json_data, headers=headers.update(default_headers), **kwargs)

    if response.ok:
        byte_array_content = response.content
        return byte_array_content.decode(encoding) if decode and encoding is not None else byte_array_content
    else:
        exc = HTTPException('%s - %s' % (response.status_code, response.reason))
        exc.status = response.status_code
        exc.reason = response.reason
        exc.headers = response.headers
        exc.url = url
        raise exc


def post_json(url, data=None, json_data=None, headers={}, encoding='utf-8', json_kwargs={}, **kwargs):
    content = post(url, data, json_data, headers=headers, encoding=encoding, **kwargs)
    print("content=[", content, "]")
    return json.loads(content, **json_kwargs)


def put(url, data=None, json_data=None, headers={}, encoding='utf-8', **kwargs):
    raise NotImplementedError()


def put_json(url, data=None, json_data=None, headers={}, encoding='utf-8', json_kwargs={}, **kwargs):
    raise NotImplementedError()


def delete(url, headers={}, encoding='utf-8', decode=True, **kwargs):
    raise NotImplementedError()


def delete_json(url, headers={}, encoding='utf-8', json_kwargs={}, **kwargs):
    raise NotImplementedError()
