import os
import hashlib

import uvicorn

from starlette.applications import Starlette
from starlette import status
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import FileResponse, PlainTextResponse, JSONResponse

from preview_generator.manager import PreviewManager


UPLOAD_DIR = '/tmp/files/'
CACHE_PATH = '/tmp/cache/'


manager = PreviewManager(CACHE_PATH, create_folder=True)


def error_response(error_message, status=None):
    return JSONResponse({"error": error_message}, status_code=status)


async def _store_uploaded_file(file) -> str:
    contents = await file.read()
    h = hashlib.md5(contents).hexdigest()
    upload_dest = os.path.join(UPLOAD_DIR, '.'.join([h, file.filename]))

    with open(upload_dest, 'wb+') as f:
        f.write(contents)

    return upload_dest


async def health_endpoint(request):
    return PlainTextResponse('OK')


async def preview_endpoint(request):
    width = request.path_params['width']
    height = request.path_params['height']

    form = await request.form()
    file = form.get('file', None)
    if file is None:
        return error_response('"file" is missing', status.HTTP_400_BAD_REQUEST)
    file_path = await _store_uploaded_file(file)

    try:
        image = manager.get_jpeg_preview(file_path, width=width, height=height)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    return FileResponse(image)


app = Starlette(routes=[
    Route('/', endpoint=health_endpoint),
    Route('/preview/{width:int}x{height:int}',
          endpoint=preview_endpoint, methods=['POST']),
])

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
