# django-chunky-upload

<p align="center">
<a href="https://github.com/Vader19695/django-chunky-upload/actions"><img alt="Actions Status" src="https://github.com/Vader19695/django-chunky-upload/workflows/Testing/badge.svg"></a>
<a href="https://pypi.org/project/django-chunky-upload/"><img alt="PyPi Version" src="https://badgen.net/pypi/v/django-chunky-upload?icon=pypi"/></a>
<a href='https://coveralls.io/github/Vader19695/django-chunky-upload?branch=readme-updates'><img src='https://coveralls.io/repos/github/Vader19695/django-chunky-upload/badge.svg?branch=readme-updates' alt='Coverage Status' /></a>
<a href="https://github.com/Vader19695/django-chunky-upload"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

This simple django app enables users to upload large files to Django in multiple chunks, with the ability to resume if the upload is interrupted.

This app is intended to work with [JQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload>) by [Sebastian Tschan](https://blueimp.net) ([documentation](https://github.com/blueimp/jQuery-File-Upload/wiki)).

License: [MIT-Zero](https://romanrm.net/mit-zero>)

This is forked from the wonderful work done in [django-chunked-upload](https://github.com/juliomalegria/django-chunked-upload).

## Installation

Install via pip:

```bash
pip install django-chunky-upload
```

And then add it to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    # ...
    'chunky_upload',
)
```

## Typical usage

1. An initial PUT request is sent to the url linked to `ChunkedUploadView` (or any subclass) with the first chunk of the file. The name of the chunk file can be overriden in the view (class attribute `field_name`). Example:

```json
{
  "my_file": "<File>"
}
```

2. In return, server will respond with the `upload_id`, the current `offset` and the when will the upload expires (`expires`). Example:

```json
{
  "upload_id": "5230ec1f59d1485d9d7974b853802e31",
  "offset": 10000,
  "expires": "2013-07-18T17:56:22.186Z"
}
```

3. Repeatedly PUT subsequent chunks using the `upload_id` to identify the upload to the url linked to `ChunkedUploadView` (or any subclass). Example:

```json
{
  "my_file": "<File>"
}
```

4. Server will continue responding with the `upload_id`, the current `offset` and the expiration date (`expires`).

5. Finally, when upload is completed, a POST request is sent to the url linked to `ChunkedUploadView` (or any subclass). This request must include the the `md5` checksum (hex). Example:

```json
{
  "md5": "fc3ff98e8c6a0d3087d515c0473f8677"
}
```

6. If everything is OK, server will respond with status code 200 and the data returned in the method `get_response_data` (if any).

Possible error responses:

- User is not authenticated. Server responds 403 (Forbidden).
- Upload has expired. Server responds 410 (Gone).
- `upload_id` does not match any upload. Server responds 404 (Not found).
- No chunk file is found in the indicated key. Server responds 400 (Bad request).
- Request does not contain `Content-Range` header. Server responds 400 (Bad request).
- Size of file exceeds limit (if specified). Server responds 400 (Bad request).
- Offsets does not match. Server responds 400 (Bad request).
- `md5` checksums does not match. Server responds 400 (Bad request).
