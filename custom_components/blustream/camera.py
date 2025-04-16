"""Platform for media_player integration."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
import logging
import time

import httpx
from pyblustream.matrix import Matrix

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo, format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.httpx_client import get_async_client

from .const import DOMAIN
from .guest_command import register_guest_command_service

_LOGGER = logging.getLogger(__name__)

SERVICE_NAME = "send_input_guest_command"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add camera for input for passed config_entry in HA."""
    register_guest_command_service(SERVICE_NAME)
    # The hub is loaded from the associated hass.data entry that was created in the
    # __init__.async_setup_entry function
    matrix: Matrix = config_entry.runtime_data

    name = config_entry.data[CONF_NAME]

    _LOGGER.debug("Setting up matrix camera entities for %s", name)

    outputs = []

    # Setup the individual output entites
    for input_id, input_name in matrix.inputs_by_id.items():
        _LOGGER.debug(
            "Setting up output entity for output_id: %s, %s", input_id, input_name
        )
        matrix_input = MatrixInputCam(input_id, input_name, matrix)
        outputs.append(matrix_input)

    async_add_entities(outputs)


class MatrixInputCam(Camera):
    """Represents the Input Previews of the Matrix."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_name = None

    _attr_frame_interval = 5
    content_type = "image/jpeg"
    access_tokens = [""]
    is_on = True
    _last_url = None
    _last_image = None
    _last_update = None

    def __init__(self, input_id, input_name, matrix) -> None:
        """Init."""
        super().__init__()
        self.input_id = input_id
        self._matrix: Matrix = matrix

        mac = format_mac(self._matrix.mac)
        self._attr_unique_id = f"{mac}-input{input_id}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=input_name,
            manufacturer="Blustream",
            configuration_url=f"http://{self._matrix.hostname}",
            model=self._matrix.device_name,
            sw_version=self._matrix.firmware_version,
            via_device=(DOMAIN, mac),
        )
        self._update_lock = asyncio.Lock()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response from the camera."""

        url = self.make_media_image_url()

        if url == self._last_url and self._limit_refetch:
            return self._last_image

        async with self._update_lock:
            if (
                self._last_image is not None
                and url == self._last_url
                and self._last_update + timedelta(0, self._attr_frame_interval)
                > datetime.now()
            ):
                return self._last_image

            try:
                update_time = datetime.now()
                async_client = get_async_client(self.hass, verify_ssl=False)
                response = await async_client.get(
                    url,
                    follow_redirects=True,
                    timeout=3,
                )
                response.raise_for_status()
                self._last_image = response.content
                self._last_update = update_time

            except httpx.TimeoutException:
                _LOGGER.error("Timeout getting camera image from %s", self._name)
                return self._last_image
            except (httpx.RequestError, httpx.HTTPStatusError) as err:
                _LOGGER.error(
                    "Error getting new camera image from %s: %s", self._name, err
                )
                return self._last_image

            self._last_url = url
            return self._last_image

    def make_media_image_url(self) -> str:
        """Return the media image URL."""
        return (
            f"{self._matrix.get_input_image_url(self.input_id)}&time={int(time.time())}"
        )

    def async_send_guest_command(self, command):
        """Send a guest command to the camera."""
        self._matrix.send_guest_command(True, self.input_id, command)
