from pychonet.echonetapiclient import ECHONETAPIClient  # noqa
from pychonet.lib.eojx import EOJX_CLASS

from .EchonetInstance import EchonetInstance
from .ElectricBlind import ElectricBlind
from .ElectricLock import ElectricLock
from .ElectricVehicleCharger import ElectricVehicleCharger
from .GeneralLighting import GeneralLighting
from .HomeAirCleaner import HomeAirCleaner
from .HomeAirConditioner import HomeAirConditioner
from .HomeSolarPower import HomeSolarPower
from .StorageBattery import StorageBattery
from .TemperatureSensor import TemperatureSensor
from .DistributionPanelMeter import DistributionPanelMeter
from .HybridWaterHeater import HybridWaterHeater

def Factory(host, server, eojgc, eojcc, eojci=0x01):
    instance = None
    if eojgc in EOJX_CLASS:
        if eojcc in EOJX_CLASS[eojgc]:
            instance = EOJX_CLASS[eojgc][eojcc]

    """Factory Method"""
    # TODO - probably a much cleaner way of doing this.
    instances = {
        "Home air conditioner": HomeAirConditioner,
        "Home solar power generation": HomeSolarPower,
        "Distribution panel metering": DistributionPanelMeter,
        "Electric vehicle charger/discharger": ElectricVehicleCharger,
        "Temperature sensor": TemperatureSensor,
        "Storage Battery": StorageBattery,
        "Electrically operated blind/shade": ElectricBlind,
        "General lighting": GeneralLighting,
        "Electric Lock": ElectricLock,
        "Air cleaner": HomeAirCleaner,
        "Hybrid Water Heater": HybridWaterHeater,
        None: None,
    }
    instance_object = instances.get(instance, None)
    if instance_object is not None:
        return instance_object(host, server, eojci)

    return EchonetInstance(host, eojgc, eojcc, eojci, server)
