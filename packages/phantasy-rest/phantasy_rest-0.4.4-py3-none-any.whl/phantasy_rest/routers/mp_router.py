#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from typing import Optional
# from db.dals.device_dal import DeviceDAL
from phantasy_rest.db.dals.device_dal import MachinePortal
from phantasy_rest.db.models.device import get_device_info
from phantasy_rest.db.models.device import HandleName
# from db.models.device import Device
from fastapi import APIRouter, Depends
from phantasy_rest.dependencies import get_device_dal

router = APIRouter()


@router.get("/devices")
async def get_all_devices(
    name: Optional[str] = '*',
    type: Optional[str] = '*',
    device_dal: MachinePortal = Depends(get_device_dal)
) -> List[str]:
    """Get a list of device names."""
    return [i.name for i in device_dal.get_elements(name=name, type=type)]


@router.get("/devices/{name}")
async def get_device(name: str,
                     device_dal: MachinePortal = Depends(get_device_dal)):
    """Get device info."""
    elems = device_dal.get_elements(name=name)
    if elems == []:
        return None
    elem = elems[0]
    return get_device_info(elem)


@router.get("/devices/attr/{name}")
async def get_attr(name: str,
                   attr: str,
                   device_dal: MachinePortal = Depends(get_device_dal)):
    """Get device attribute value."""
    elems = device_dal.get_elements(name=name)
    if elems == []:
        val = "Non-existing device"
    else:
        elem = elems[0]
        if hasattr(elem, attr):
            val = getattr(elem, attr)
        else:
            val = "Non-existing attribute"
    return {"name": name, "attr": attr, "value": val}


@router.get("/devices/value/{name}")
async def get_value(name: str,
                    field: str,
                    handle: Optional[HandleName] = "readback",
                    device_dal: MachinePortal = Depends(get_device_dal)):
    """Get device field value."""
    elems = device_dal.get_elements(name=name)
    if elems == []:
        val = "Non-existing device"
    else:
        elem = elems[0]
        if handle == 'readback':
            if field in elem.fields:
                val = getattr(elem, field)
            else:
                val = "Non-existing field"
        else:
            if field in elem.fields:
                val = elem.current_setting(field)
            else:
                val = "Non-existing field"
    return {"name": name, "field": field, "value": val, "handle": handle}


@router.put("/devices/value/{name}")
async def set_value(name: str,
                    field: str,
                    value: float,
                    device_dal: MachinePortal = Depends(get_device_dal)):
    """Set device field to value.
    """
    elems = device_dal.get_elements(name=name)
    if elems == []:
        return "Non-existing device"
    elem = elems[0]
    if field not in elem.fields:
        return "Non-existing field"
    setattr(elem, field, value)
    return f"Set {name} [{field}] to {value}"


@router.post("/devices/convert/{name}")
async def convert(name: str,
                  field: str,
                  value: float,
                  to_field: Optional[str] = None,
                  device_dal: MachinePortal = Depends(get_device_dal)):
    """Convert value of field to the value of to_field of device.
    """
    elems = device_dal.get_elements(name=name)
    if elems == []:
        return "Non-existing device"
    elem = elems[0]
    if to_field is None:
        to_field = sorted(
            filter(lambda x: x[0] == field, elem._CaElement__unicorn))[0][-1]
    val = elem.convert(value, from_field=field, to_field=to_field)
    return {"value": val, "to_field": to_field}


@router.get("/devices/fields/{name}")
async def fields(name: str,
                 device_dal: MachinePortal = Depends(get_device_dal)):
    """Return a list of field names attached to the element.
    """
    elems = device_dal.get_elements(name=name)
    if elems == []:
        return "Non-existing device"
    elem = elems[0]
    return elem.fields


@router.get("/devices/pv/{name}")
async def get_pv(name: str,
                 field: str,
                 handle: Optional[HandleName] = "readback",
                 device_dal: MachinePortal = Depends(get_device_dal)):
    """Return a list of PV names that point to the given field of an element.
    """
    elems = device_dal.get_elements(name=name)
    if elems == []:
        return "Non-existing device"
    elem = elems[0]
    return elem.pv(field, handle=handle)



