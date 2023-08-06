#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" EPICS routers """
from typing import Optional
from fastapi import APIRouter
import aioca

router = APIRouter()


@router.get("/epics/caget")
async def caget(pvname: str, datatype: Optional[str] = None):
    """Get the value of a PV through CA.
    """
    # datatype: https://dls-controls.github.io/aioca/master/api.html#augmented-values
    if datatype in ("", "none", "None"):
        datatype = None
    return await aioca.caget(pvname, datatype=datatype)

@router.post("/epics/caput")
async def caput(pvname: str, value):
    """Set PV with a new value through CA.
    """
    return await aioca.caput(pvname, value, throw=False)

