from pathlib import Path

from fastapi import FastAPI, Request, File, UploadFile, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from server.pdf2jpg import convertPDF

app = FastAPI()

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

print(Path(__file__).parent.parent.absolute())

# -------------------------------------HTML Templates-------------------------------------
@app.get('/')
def login(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})


# --------------------------------------API Requests--------------------------------------
@app.post("/convert_to_pdf")
async def upload_file(request: Request, file: UploadFile = File(...)):
    zip_bytes = await convertPDF(file)    
    return Response(content=zip_bytes, media_type="application/zip")



# To run the app for development: python -m uvicorn server.server:app --host 0.0.0.0 --reload
# To run the app on AWS: python3 -m uvicorn server.server:app