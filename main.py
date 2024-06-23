#!/usr/bin/env python3
from fastapi import Depends
from sqlalchemy.orm import Session

from app import create_app
from app.db.db import get_db

app = create_app()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None, db: Session = Depends(get_db)):
    return {'item_id': item_id, 'q': q}


if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
