from dataclasses import dataclass, field
import io
import struct

from pointevector.zip.exceptions import BadMagic, IncompleteParse

@dataclass(frozen=True)
class FileHeader:
    min_version_needed: int
    bit_flags: bytes
    compression_method: int
    last_modified_time: bytes
    last_modified_date: bytes
    uncompressed_checksum: bytes
    compressed_size: int
    uncompressed_size: int
    filename_length: int
    extra_field_length: int
    filename: str=''
    extra_field: bytes=b''
    MAGIC_NUMBER: bytes=field(default=b'PK\x03\x04', init=False, repr=False)
    STATIC_FORMAT: str=field(default=r'<4sH2sH2s2s4s2L2H', init=False, repr=False)

    @classmethod
    def from_stream(cls, stream: io.BytesIO):
        s = struct.unpack(cls.STATIC_FORMAT, stream.read(struct.calcsize(cls.STATIC_FORMAT)))
        if s[0] == cls.MAGIC_NUMBER:
            filename = stream.read(s[9])
            if len(filename) < s[9]:
                raise IncompleteParse()
            extra_field = stream.read(s[10])
            if len(extra_field) < s[10]:
                raise IncompleteParse()
            return cls(*s[1:], filename.decode(), extra_field)
        else:
            raise BadMagic()

@dataclass(frozen=True)
class DataDescriptor:
    uncompressed_checksum: bytes
    compressed_size: int
    uncompressed_size: int
    MAGIC_NUMBER: bytes=field(default=b'PK\x07\x08', init=False, repr=False)
    STATIC_FORMAT: str=field(default=r'<4s4s2L', init=False, repr=False)

    @classmethod
    def from_stream(cls, stream: io.BytesIO):
        s = struct.unpack(cls.STATIC_FORMAT, stream.read(struct.calcsize(cls.STATIC_FORMAT)))
        if s[0] == cls.MAGIC_NUMBER:
            return cls(*s[1:])
        else:
            raise BadMagic()

@dataclass(frozen=True)
class CDHeader:
    version_created_by: int
    min_version_needed: int
    bit_flags: bytes
    compression_method: int
    last_modified_time: bytes
    last_modified_date: bytes
    uncompressed_checksum: bytes
    compressed_size: int
    uncompressed_size: int
    filename_length: int
    extra_field_length: int
    comment_length: int
    file_start_disk: int
    internal_file_attributes: bytes
    external_file_attributes: bytes
    local_file_header_offset: int
    filename: str=''
    extra_field: bytes=b''
    comment: str=''
    MAGIC_NUMBER: bytes=field(default=b'PK\x01\x02', init=False, repr=False)
    STATIC_FORMAT: str=field(default=r'<4s2H2sH2s2s4s2L4H2s4sL', init=False, repr=False)

    @classmethod
    def from_stream(cls, stream: io.BytesIO):
        s = struct.unpack(cls.STATIC_FORMAT, stream.read(struct.calcsize(cls.STATIC_FORMAT)))
        if s[0] == cls.MAGIC_NUMBER:
            filename = stream.read(s[10]).decode()
            if len(filename) < s[10]:
                raise IncompleteParse()
            extra_field = stream.read(s[11])
            if len(extra_field) < s[11]:
                raise IncompleteParse()
            comment = stream.read(s[12]).decode()
            if len(comment) < s[12]:
                raise IncompleteParse()
            return cls(*s[1:], filename, extra_field, comment)
        else:
            raise BadMagic()

@dataclass(frozen=True)
class EOCD:
    disk_number: int
    cd_disk: int
    cd_records_on_disk: int
    total_cd_records: int
    cd_size: int
    cd_start_offset: int
    comment_length: int
    comment: str=''
    MAGIC_NUMBER: bytes=field(default=b'PK\x05\x06', init=False, repr=False)
    STATIC_FORMAT: str=field(default=r'<4s4H2LH', init=False, repr=False)

    @classmethod
    def from_stream(cls, stream: io.BytesIO):
        s = struct.unpack(cls.STATIC_FORMAT, stream.read(struct.calcsize(cls.STATIC_FORMAT)))
        if s[0] == cls.MAGIC_NUMBER:
            comment = stream.read(s[7]).decode()
            if len(comment) != s[7]:
                raise IncompleteParse()
            return cls(*s[1:], comment)
        else:
            raise BadMagic()
