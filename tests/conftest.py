import sys
import os
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


os.chdir(os.getcwd()+'/api/')
sys.path.append(os.getcwd())

os.environ['PROJECT_NAME'] = 'test'
os.environ['SERVER'] = 'http://localhost/api/'
os.environ['CLIENT'] = 'http://localhost/'
os.environ['MODE'] = 'test'
os.environ['TG_TOKEN'] = '123456789:AABBCCDDEEFFaabbccddeeff-1234567890'


@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    from app import app
    yield app

@pytest.fixture(scope='function')
def client(
    app: FastAPI,
) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client
