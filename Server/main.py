from fastapi import FastAPI
from fastapi_cdn_host import monkey_patch_for_docs_ui 

from models import m_user
from config.database import engine
from routes import user, auth
from data.email import send_with_template, EmailSchema

m_user.Base.metadata.create_all(bind=engine)
app = FastAPI()
monkey_patch_for_docs_ui(app)

@app.get("/")
async def root():
    await send_with_template(
        EmailSchema(
            email="test-4b705022@appmaildev.com",
            body={"verify_code": "46454"},
            type="verify-first"
        )
    )
    return {"message": "Hello World"}

app.include_router(user.users_router, prefix="/user")
app.include_router(auth.auth_router, prefix="/auth")