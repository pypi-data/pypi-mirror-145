from abc import ABC, abstractmethod
from enum import Enum
import logging
import io
import struct
import zlib

from pointevector.zip.core import DataDescriptor, FileHeader, CDHeader, EOCD, IncompleteParse

class StreamParser(ABC):
    class State(Enum):
        UNKNOWN = 0
        LOCAL_HEADER = 1
        CONTENT = 2
        DATA_DESCRIPTOR = 3
        CD_HEADER = 4
        EOCD = 5

    def __init__(self):
        self.zip_state = StreamParser.State.UNKNOWN
        self.buffer = io.BytesIO()
        self.decompressor = None

    @abstractmethod
    def local_header(self, data: FileHeader):
        pass

    @abstractmethod
    def file_content(self, data: bytes):
        pass

    @abstractmethod
    def data_descriptor(self, data: DataDescriptor):
        pass

    @abstractmethod
    def cd_header(self, data: CDHeader):
        pass

    @abstractmethod
    def eocd(self, data: EOCD):
        pass

    def feed(self, data: bytes):
        # Update buffer
        self.buffer.seek(self.buffer.getbuffer().nbytes)
        self.buffer.write(data)

        # Process buffer
        while True:
            # Unknown
            if self.zip_state == StreamParser.State.UNKNOWN:
                # Ensure there is enough data in the buffer
                if self.buffer.getbuffer().nbytes < 4:
                    break
                self.buffer.seek(0)
                magic = self.buffer.read(4)
                if magic == FileHeader.MAGIC_NUMBER:
                    self.zip_state = StreamParser.State.LOCAL_HEADER
                elif magic == DataDescriptor.MAGIC_NUMBER:
                    self.zip_state = StreamParser.State.DATA_DESCRIPTOR
                elif magic == CDHeader.MAGIC_NUMBER:
                    self.zip_state = StreamParser.State.CD_HEADER
                elif magic == EOCD.MAGIC_NUMBER:
                    self.zip_state = StreamParser.State.EOCD
                else:
                    logging.critical('bad state')
                    raise Exception(magic)
            # Local Header
            elif self.zip_state == StreamParser.State.LOCAL_HEADER:
                # Ensure there is enough data in the buffer
                if self.buffer.getbuffer().nbytes < struct.calcsize(FileHeader.STATIC_FORMAT):
                    break
                self.buffer.seek(0)
                try:
                    data = FileHeader.from_stream(self.buffer)
                except IncompleteParse:
                    break
                self.local_header(data)
                self.buffer = io.BytesIO(self.buffer.read())
                # Prepare CONTENT state
                self.decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
                self.content = io.BytesIO()
                self.zip_state = StreamParser.State.CONTENT
            # Content
            elif self.zip_state == StreamParser.State.CONTENT:
                self.buffer.seek(0)
                data = self.decompressor.decompress(self.buffer.read())
                self.file_content(data)
                # Reset buffer
                self.buffer = io.BytesIO(self.decompressor.unused_data)
                # Transition to UNKNOWN state
                if self.decompressor.eof:
                    self.zip_state = StreamParser.State.UNKNOWN
                else:
                    # Get more data
                    break
            # Data Descriptor
            elif self.zip_state == StreamParser.State.DATA_DESCRIPTOR:
                # Ensure there is enough data in the buffer
                if self.buffer.getbuffer().nbytes < struct.calcsize(DataDescriptor.STATIC_FORMAT):
                    break
                # Read DataDescriptor
                self.buffer.seek(0)
                data = DataDescriptor.from_stream(self.buffer)
                self.data_descriptor(data)
                self.buffer = io.BytesIO(self.buffer.read())
                # Transition to UNKNOWN state
                self.zip_state = StreamParser.State.UNKNOWN
            # Central Directory File Header
            elif self.zip_state == StreamParser.State.CD_HEADER:
                # Ensure there is enough data in the buffer
                if self.buffer.getbuffer().nbytes < struct.calcsize(CDHeader.STATIC_FORMAT):
                    break
                self.buffer.seek(0)
                try:
                    data = CDHeader.from_stream(self.buffer)
                except IncompleteParse:
                    break
                self.cd_header(data)
                self.buffer = io.BytesIO(self.buffer.read())
                # Transition to UNKNOWN state
                self.zip_state = StreamParser.State.UNKNOWN
            # End Of Central Directory Record
            elif self.zip_state == StreamParser.State.EOCD:
                # Ensure there is enough data in the buffer
                if self.buffer.getbuffer().nbytes < struct.calcsize(EOCD.STATIC_FORMAT):
                    break
                self.buffer.seek(0)
                try:
                    data = EOCD.from_stream(self.buffer)
                except IncompleteParse:
                    break
                self.eocd(data)
                self.buffer = io.BytesIO(self.buffer.read())
                # Transition to UNKNOWN state
                self.zip_state = StreamParser.State.UNKNOWN
            else:
                logging.critical('Bad state')
                raise Exception()
