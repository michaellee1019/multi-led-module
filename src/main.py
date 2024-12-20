import asyncio
from typing import ClassVar, Final, Mapping, Sequence, Optional
from smbus2 import SMBus, i2c_msg

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

import json
import io

LOG = logging.getLogger(__name__)
MESSAGE_CHUNK_SIZE = 32

# used to divide a byte string into 32 byte chunks to send over i2c and then put back together on the read side
def divide_chunks(l, n):
    
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]


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
        if "num_strands" not in config.attributes.fields:
            raise Exception("A num_strands attribute is required for multi led component. Must be an integer. This is the number of led strips")

        if "strand_length" not in config.attributes.fields:
            raise Exception("A strand_length attribute is required for multi led component. Must be an integer. This is the number of pixels per strip.")
        
        if "brightness" not in config.attributes.fields:
            raise Exception("A brightness attribute is required for multi led component component. Must be a float like 0.2 for 20% brightness")

        if "address" not in config.attributes.fields:
            raise Exception("A address attribute is required for multi led component. It should be of format 0xADDRESS")
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
        address_hex_string = config.attributes.fields["address"].string_value
        LOG.info(f"address hex string: {address_hex_string}")
        address = int(address_hex_string, 16)
        LOG.info(f"converted address: {address}")

        
        if self.bus is not None:
            self.bus.close()
        
        self.bus = SMBus(1)
        pixel_config = {
            "num_strands": num_strands,
            "strand_length": strand_length,
            "brightness": brightness
        }
        
        self.num_strands = num_strands
        self.strand_length = self.strand_length
        self.brightness = brightness
        self.address = address
        
        self.send_message(pixel_config)
        
    async def do_command(
            self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None,**kwargs,
    ) -> Mapping[str, ValueTypes]:
        LOG.info("do command tings")
        LOG.info(f"value passed into do command: {command}")
        
    def send_message(self, message):
        byte_string = json.dumps(message).encode("utf-8")
        chunks = divide_chunks(byte_string, MESSAGE_CHUNK_SIZE)
        for chunk in chunks:
            self.bus.write_i2c_block_data(self.address, 0x00, chunk)
        LOG.info("sent message over i2c")

if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
