#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from phantasy import CaElement

ATTR_MAP = {
    'name': 'name',
    'type': 'family',
    'physics_name': 'phy_name',
    'physics_type': 'phy_type',
    'pos_begin': 'sb',
    'pos_end': 'se',
    'length': 'length',
    'tags': 'tags',
    'fields': 'fields'
}


class HandleName(str, Enum):
    readback = "readback"
    setpoint = "setpoint"


def get_device_info(elem: CaElement):
    return {k: getattr(elem, v) for k, v in ATTR_MAP.items()}


# from sqlalchemy import Column, Integer, String
# from db.config import Base

# class Device(Base):
#     __tablename__ = "Devices"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     family = Column(String, nullable=False)
