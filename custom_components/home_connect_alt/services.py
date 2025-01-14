""" Implement the services of this implementation """
from home_connect_async import HomeConnect
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr


class Services():
    """ Collection of the Services offered by the integration """
    def __init__(self, hass:HomeAssistant,  homeconnect:HomeConnect) -> None:
        self.homeconnect = homeconnect
        self.hass = hass
        self.dr = dr.async_get(hass)

    async def async_select_program(self, call) -> None:
        """ Service for selecting a program """
        data = call.data
        appliance = self.get_appliance_from_device_id(data['device_id'])
        if appliance:
            program_key = data['program_key']
            options = data.get('options')

            await appliance.async_select_program(key=program_key, options=options )

    async def async_start_program(self, call) -> None:
        """ Service for starting the currently selected program """
        data = call.data
        appliance = self.get_appliance_from_device_id(data['device_id'])
        if appliance:
            await appliance.async_start_program()

    async def async_stop_program(self, call) -> None:
        """ Service for stopping the currently active program """
        data = call.data
        appliance = self.get_appliance_from_device_id(data['device_id'])
        if appliance:
            await appliance.async_stop_active_program()

    def get_appliance_from_device_id(self, device_id):
        """ Helper function to get an appliance from the Home Assistant device_id """
        device = self.dr.devices[device_id]
        haId = list(device.identifiers)[0][1]
        for (key, appliance) in self.homeconnect.appliances.items():
            if key.lower().replace('-','_') == haId:
                return appliance
        return None
