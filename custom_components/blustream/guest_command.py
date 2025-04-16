from homeassistant.helpers import entity_platform
import homeassistant.helpers.config_validation as cv
import voluptuous as vol


async def send_guest_command(entity, service_call):
    """Send a serial guest command through the ACM."""
    command_bytes = service_call.data["command_string_bytes"]
    command = bytes(command_bytes)
    if b"CLOSEACMGUEST" in command:
        raise ValueError("Cannot exit guest mode manually")
    entity.async_send_guest_command(command)


def register_guest_command_service(service_name):
    """Register the guest command service."""
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        service_name,
        {
            vol.Required("command_string_bytes"): vol.All(
                cv.ensure_list,
                [cv.byte],
            ),
        },
        send_guest_command,
    )
