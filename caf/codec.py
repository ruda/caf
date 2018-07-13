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

"""Encode or decode Core Audio Format (CAF) files.

https://developer.apple.com/library/archive/documentation/MusicAudio/Reference/CAFSpec/
"""

import collections
import struct

from uuid import UUID

from . import Error, Reader, Writer


CAFdesc    = collections.namedtuple('CAFdesc', 'sample_rate format_id format_flags bytes_per_packet frames_per_packet channels_per_frame bits_per_channel')
CAFkuki    = collections.namedtuple('CAFkuki', 'cookie_data')
CAFdata    = collections.namedtuple('CAFdata', 'edit_count data')
CAFpakt    = collections.namedtuple('CAFpakt', 'number_packets number_valid_frames priming_frames remainder_frames data')
CAFinst    = collections.namedtuple('CAFinst', 'base_note midi_low_note midi_high_note midi_low_velocity midi_high_velocity db_gain start_region_id sustain_region_id release_region_id instrument_id')
CAFmidi    = collections.namedtuple('CAFmidi', 'data')
CAFinfo    = collections.namedtuple('CAFinfo', 'key value')
CAFovvw    = collections.namedtuple('CAFovvw', 'edit_count num_frames_per_ovw_sample data')
CAFuuid    = collections.namedtuple('CAFuuid', 'uuid data')
CAFfree    = collections.namedtuple('CAFfree', 'data')

CAFStringsChunk = collections.namedtuple('CAFStringsChunk', 'num_entries strings')
CAFStrings      = collections.namedtuple('CAFStrings', 'num_entries strings_ids strings')
CAFStringId     = collections.namedtuple('CAFStringID', 'string_id string_start_byte_offset')



class ChunkDecoder(object):
    """Decode chunk and data."""

    def __init__(self, chunk=None, data=None):
        self.chunk = chunk
        self.data  = data

    def decode(self):
        try:
            decode_chunk_fn = getattr(self, '_decode_chunk_' + self.chunk.chunk_type)
        except AttributeError:
            raise Error, "unimplemented decoder for chunk type '%s'" % self.chunk.chunk_type
        return decode_chunk_fn()


class RealChunkDecoder(ChunkDecoder):
    """Decode chunk and data."""

    def _decode_chunk_desc(self):
        return CAFdesc._make(struct.unpack('>d4sLLLLL', self.data))

    def _decode_chunk_data(self):
        edit_count = struct.unpack('>L', self.data[0:4])
        data = self.data[4:]
        return CAFdata(edit_count, data)

    def _decode_chunk_kuki(self):
        return CAFkuki(self.data)

    def _decode_chunk_info(self):
        num_entries,  = struct.unpack('>L', self.data[0:4])
        strings = self.data[4:]
        return CAFinfo(num_entries, strings)

    def _decode_chunk_pakt(self):
        a, b, c, d = struct.unpack('>qqii', self.data[0:24])
        data = self.data[24:]
        return CAFpakt(a, b, c, d, data)

    def _decode_chunk_inst(self):
        return CAFinst(struct.unpack('>fBBBBfLLLL'), self.data)

    def _decode_chunk_midi(self):
        return CAFmidi(self.data)

    def _decode_chunk_ovvw(self):
        edit_count, num_frames_per_ovw_sample = struct.unpack('>II', self.data[0:8])
        data = self.data[8:]
        return CAFovvw(edit_count, num_frames_per_ovw_sample, data)

    def _decode_chunk_uuid(self):
        uuid = UUID(bytes=self.data[0:16])
        data = self.data[16:]
        return CAFuuid(uuid, data)

    def _decode_chunk_free(self):
        return CAFfree(self.data)


class Decoder(object):
    """Decode chunks from CAF file."""

    def __init__(self, f, decoder=None):
        if decoder is None:
            decoder = RealChunkDecoder
        self.chunk_reader = Reader(f)
        self.chunk_decoder = decoder

    def __iter__(self):
        for chunk, data in self.chunk_reader:
            yield self.chunk_decoder(chunk, data).decode()


class Encoder(object):
    """Encode chunks to CAF file."""

    def __init__(self, f, encoder=None):
        if encoder is None:
            encoder = RealChunkEncoder
        self.chunk_writer = writer(f)
        self.chunk_encoder = encoder


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        fp = sys.stdin
    else:
        fp = open(sys.argv[1], 'rb')
    try:
        caf = open(fp)
    except Error as err:
        print err
    else:
        for part in caf:
            print part
