from fastapi import FastAPI
from app.user import user_router
from app.authors import authors_router
from app.Books import books_router
from app.common.config.database import engine, Base
import subprocess
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)
app = FastAPI()

# origins = [
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
#     "http://localhost:8080",
#     "null"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.app)
app.include_router(authors_router.app)
app.include_router(books_router.app)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthcheck")
def healthz():
    return True

def run_streamlit():
    subprocess.Popen(["streamlit", "run", "/Users/aalyousef001/My_Smart_Library/Smart-Library/app/llama/chatbot.py"])

if __name__ == "__main__":
    # run_streamlit()
    uvicorn.run(app, host="0.0.0.0", port=8000)
