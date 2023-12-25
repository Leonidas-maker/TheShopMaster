from fastapi import FastAPI

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute() / "config"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "models"))
sys.path.append(str(Path(__file__).parent.parent.absolute() / "routes"))

from models import m_user
from database import engine
from routes import user, auth

m_user.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user.users_router, prefix="/user")
app.include_router(auth.auth_router, prefix="/auth")