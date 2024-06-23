def create_app():
    from fastapi import FastAPI
    from app import frontend
    app = FastAPI()
    frontend.init(app)
    return app
