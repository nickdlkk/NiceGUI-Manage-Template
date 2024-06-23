#!/usr/bin/env python3
import uvicorn

# app = create_app()
#
#
# @app.get('/')
# def read_root():
#     return {'Hello': 'World'}
#
#
# @app.get('/items/{item_id}')
# def read_item(item_id: int, q: str = None, db: Session = Depends(get_db)):
#     return {'item_id': item_id, 'q': q}


if __name__ == '__main__':
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info")
