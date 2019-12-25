import os
import hashlib

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import FileResponse, PlainTextResponse

from preview_generator.manager import PreviewManager


UPLOAD_DIR = '/tmp/files/'
CACHE_PATH = '/tmp/cache/'


manager = PreviewManager(CACHE_PATH, create_folder=True)


async def _store_uploaded_file(file) -> str:
    contents = await file.read()
    h = hashlib.md5(contents).hexdigest()
    upload_dest = os.path.join(UPLOAD_DIR, h)

    with open(upload_dest, 'wb') as f:
        f.write(contents)

    return upload_dest


async def health_endpoint(request):
    return PlainTextResponse('OK')


async def preview_endpoint(request):
    width = request.path_params['width']
    height = request.path_params['height']

    form = await request.form()
    file_path = await _store_uploaded_file(form['file'])

    image = manager.get_jpeg_preview(file_path, width=width, height=height)

    return FileResponse(image)


app = Starlette(routes=[
    Route('/', endpoint=health_endpoint),
    Route('/preview/{width:int}x{height:int}',
          endpoint=preview_endpoint, methods=['POST']),
])
