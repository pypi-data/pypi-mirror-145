from phantasy_rest._gconf import machine, segment
from phantasy import MachinePortal

mp = MachinePortal(machine, segment)


async def get_device_dal():
    yield mp
