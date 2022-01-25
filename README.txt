Python module for Core Audio Format (CAF) files.
Rudá Moura <ruda.moura@gmail.com>

INTRODUCTION

This is a very low level module to interact with Code Audio Format (CAF) files.

USAGE

Example: extracting MIDI content from CAF file using chunks.

---
import caf as caflib

caf = caflib.Reader('/Library/Audio/Apple Loops/Apple/13 Drummer/Zak - Intro.caf')

for chunk, data in caf:
    if chunk.chunk_type == b'midi': break
open('Zak - Intro.mid', 'wb').write(data)
---

Example: navigating into the parts of CAF file.

>>> import caf
>>> f = caf.open('/Library/Audio/Apple Loops/Apple/13 Drummer/Zak - Intro.caf')
>>> i = iter(f)
>>> o = next(i) ; print(o)
CAFdesc(sample_rate=44100.0, format_id=b'aac ', format_flags=0, bytes_per_packet=0, frames_per_packet=1024, channels_per_frame=2, bits_per_channel=0)
>>> print(o.sample_rate)
44100.0
>>> o = next(i) ; print(o)
CAFkuki(cookie_data=b'\x03\x80\x80\x80"\x00\x00\x00\x04\x80\x80\x80\x14@\x15\x00\x18\x00\x00\x02/\xf0\x00\x01\xf4\x00\x05\x80\x80\x80\x02\x12\x10\x06\x80\x80\x80\x01\x02')
>>> o = next(i) ; print(o)
CAFinfo(key=1, value=b'comments\x00Creator: Logic\x00')
>>> print(type(o))
<class 'caf.codec.CAFinfo'>
>>> print(type(o) == caf.codec.CAFinfo)
True

BUGS

Many, this module is incomplete.
