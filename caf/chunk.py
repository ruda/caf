# encoding: utf-8
#
# Copyright © 2018 Rudá Moura <ruda.moura@gmail.com>
#
# Permission to use, copy, modify, distribute, and sell this software and its
# documentation for any purpose is hereby granted without fee, provided that
# the above copyright notice appear in all copies and that both that
# copyright notice and this permission notice appear in supporting
# documentation.  No representations are made about the suitability of this
# software for any purpose.  It is provided "as is" without express or
# implied warranty.

"""Encode or decode chunks of Core Audio Format (CAF) files.
"""

import collections
import struct


CAFFileHeader  = collections.namedtuple('CAFFileHeader', 'file_type file_version file_flags')
CAFChunkHeader = collections.namedtuple('CAFChunkHeader', 'chunk_type chunk_size')

_FileHeaderMask, _FileHeaderSize   = '>4sHH', 8
_ChunkHeaderMask, _ChunkHeaderSize = '>4sq', 12


class Reader(object):
    """Read CAF file as a series of chunks."""

    def __init__(self, f):
        self.file_header = None
        self.chunk_header = None
        if type(f) == type(''):
            f = open(f, 'rb')
        self.file = f
        self.file_header = CAFFileHeader._make(struct.unpack(_FileHeaderMask, self.file.read(_FileHeaderSize)))
        if self.file_header.file_type != 'caff':
             raise IOError('file is not a valid CAF')

    def __iter__(self):
        while True:
            try:
                self.chunk_header = CAFChunkHeader._make(struct.unpack(_ChunkHeaderMask, self.file.read(_ChunkHeaderSize)))
            except struct.error:
                raise StopIteration
            self.data = self.file.read(self.chunk_header.chunk_size)
            assert self.chunk_header.chunk_size == len(self.data)
            yield self.chunk_header, self.data

    def __del__(self):
        self.file.close()


class Writer(object):
    """Write CAF file as a series of chunks."""

    def __init__(self, f, file_type='caff', file_version=1, file_flags=0):
        self.file_header = CAFFileHeader(file_type, file_version, file_flags)
        if type(f) == type(''):
            f = open(f, 'wb')
        self.file = f
        data = struct.pack(_FileHeaderMask, *self.file_header)
        self.file.write(data)

    def __del__(self):
        self.file.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        fp = sys.stdin
    else:
        fp = open(sys.argv[1], 'rb')
    try:
        caf = Reader(fp)
    except Exception as err:
        print err
    else:
        for chunk, data in caf:
            data = data[:32].encode('hex')
            print chunk, data
