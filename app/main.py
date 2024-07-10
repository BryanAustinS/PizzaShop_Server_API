import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)  # NOSONAR

tags_metadata = [
    {
        'name': 'user',
        'description': 'Operations with users. ',
    },
    {
        'name': 'order',
        'description': 'Operations  with orders.',
    },
    {
        'name': 'beverage',
        'description': 'Operations with beverages. ',
    },
    {
        'name': 'pizza_type',
        'description': 'Operations with pizza_types. ',
    },
    {
        'name': 'dough',
        'description': 'Operations with doughs. ',
    },
    {
        'name': 'sauce',
        'description': 'Operations with sauces. ',
    },
    {
        'name': 'topping',
        'description': 'Operations with toppings. ',
    },
]

app = FastAPI(openapi_tags=tags_metadata)

origins = [
    'http://localhost',
    'http://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=[],
)

# This function routes to version 1 of the REST API /v1/..
app.include_router(
    api_v1_router,
    prefix='/v1',
)

if __name__ == '__main__':
    logging.info('App is up and running')
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000)
