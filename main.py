#!/usr/bin/env python3
import uvicorn

from app.conf.config import Config
from app.utils.logger import get_log_config, setup_logger, get_logger

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
config = Config()
setup_logger()

logger = get_logger(__name__)

if config.log.console_log_level != "DEBUG":
    import warnings

    warnings.filterwarnings("ignore")
if __name__ == '__main__':
    uvicorn.run(app="app.app:app", host=config.http.host,
                port=config.http.port,
                proxy_headers=True,
                forwarded_allow_ips='*',
                log_config=get_log_config(),
                reload=True,
                )
