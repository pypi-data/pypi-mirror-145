from typing import List, Type

from cfinterface.components.block import Block
from cfinterface.components.defaultblock import DefaultBlock
from cfinterface.data.blockdata import BlockData
from cfinterface.reading.blockreading import BlockReading
from cfinterface.writing.blockwriting import BlockWriting


class BlockFile:
    """
    Class that models a file divided by blocks, where the reading
    and writing are given by a series of blocks.
    """

    BLOCKS: List[Type[Block]] = []

    def __init__(
        self,
        data=BlockData(DefaultBlock("")),
    ) -> None:
        self.__data = data

    def read(self, directory: str, filename: str = ""):
        """
        Reads the blockfile data from a given file in disk.

        :param filename: The file name in disk
        :type filename: str
        :param directory: The directory where the file is
        :type directory: str
        """
        reader = BlockReading(self.__class__.BLOCKS)
        self.__data = reader.read(filename, directory)

    def write(self, directory: str, filename: str = ""):
        """
        Write the blockfile data to a given file in disk.

        :param filename: The file name in disk
        :type filename: str
        :param directory: The directory where the file will be
        :type directory: str
        """
        writer = BlockWriting(self.__data)
        writer.write(filename, directory)

    @property
    def data(self) -> BlockData:
        return self.__data
