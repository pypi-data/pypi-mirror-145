#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI

from phantasy_rest.routers import mp_router
from phantasy_rest.routers import ca_router

app = FastAPI()
app.include_router(mp_router.router)
app.include_router(ca_router.router)


@app.get('/')
async def index():
    """Get package info.
    """
    import phantasy_rest
    return {
        "Package name": phantasy_rest.__name__,
        "Version": phantasy_rest.__version__,
        "Author": phantasy_rest.__author__,
        "Description": phantasy_rest.__doc__
    }


@app.get('/lattice')
async def lattice():
    """Get loaded lattice info.
    """
    from phantasy_rest._gconf import machine, segment
    return {"machine": machine, "segment": segment}


@app.get('/config')
async def config():
    """Get gunicorn configurations.
    """
    import subprocess
    import phantasy_rest
    s = subprocess.run("gunicorn --print-config main:app --config _gconf.py".split(),
                       cwd=phantasy_rest.__path__[0],
                       capture_output=True)
    return {
        k.strip(): v.strip()
        for k, v in (i.split("=")
                     for i in s.stdout.decode().strip().split("\n"))
    }


if __name__ == "__main__":
    uvicorn.run("main:app",
                port=8080,
                host="127.0.0.1",
                reload=True,
                debug=True)
