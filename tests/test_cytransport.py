# -*- coding: utf-8 -*-

import pytest

from thriftpy._compat import PYPY

pytestmark = pytest.mark.skipif(PYPY, reason="cython not enabled in pypy.")

if not PYPY:
    from thriftpy.transport.framed import TCyFramedTransport
    from thriftpy.transport.buffered import TCyBufferedTransport
    from thriftpy.transport import TMemoryBuffer, TTransportException


def test_transport_mismatch():
    s = TMemoryBuffer()

    t1 = TCyBufferedTransport(s)
    t1.write(b"\x80\x01\x00\x01\x00\x00\x00\x04ping hello world")
    t1.flush()

    with pytest.raises(TTransportException) as exc:
        t2 = TCyFramedTransport(s)
        t2.read(4)

    assert "No frame" in str(exc.value)


def test_buffered_read():
    s = TMemoryBuffer()

    t = TCyBufferedTransport(s)
    t.write(b"ping")
    t.flush()

    assert t.read(4) == b"ping"