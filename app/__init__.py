import os

from fastapi import FastAPI

from app import frontend


def create_app():
    app = FastAPI()
    frontend.init(app)
    return app
