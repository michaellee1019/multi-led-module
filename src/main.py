import asyncio
from typing import ClassVar, Final, Mapping, Sequence, Optional


from typing_extensions import Self
from viam.components.generic import *
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes
from viam import logging

import serial
import json
import io

LOG = logging.getLogger(__name__)

class MultiLed(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("vijayvuyyuru", "multi-led"), "multi-led"
    )

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Generic component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        num_strands: int = int(config.attributes.fields["num_strands"].number_value)
        strand_length: str = config.attributes.fields["strand_length"].string_value
        brightness: float = config.attributes.fields["brightness"].number_value
        ser = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=2)
        if not ser.is_open:
            ser.open()  # check and open Serial0
        ser.flush()  # clear the UART Input buffer
        self.ser = ser
        pixel_config = {
            "num_strands": num_strands,
            "strand_length": strand_length,
            "brightness": brightness
        }
        
        buffer = io.StringIO()
        json.dump(pixel_config, buffer)
        buffer.seek(0)
        self.ser.write(buffer)
        
    async def do_command(
            self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None,**kwargs,
    ) -> Mapping[str, ValueTypes]:
        LOG.info("do command tings")

if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
