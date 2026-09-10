import io

from golf_offshoot.operator_surface.client_write import is_client_abort, write_http_body


class _AbortingFile:
    def write(self, _body):
        raise ConnectionAbortedError(10053, "An established connection was aborted")


class _ResetFile:
    def write(self, _body):
        err = OSError("connection reset")
        err.winerror = 10054
        raise err


def test_connection_aborted_is_a_client_abort():
    assert is_client_abort(ConnectionAbortedError())
    assert is_client_abort(BrokenPipeError())
    err = OSError("aborted")
    err.winerror = 10053
    assert is_client_abort(err)
    assert not is_client_abort(OSError("disk full"))


def test_write_http_body_swallows_client_abort():
    logged = []
    write_http_body(_AbortingFile(), b"<html/>", log=logged.append)
    assert logged
    assert "client abort" in logged[0]


def test_write_http_body_swallows_winerror_reset():
    logged = []
    write_http_body(_ResetFile(), b"<html/>", log=logged.append)
    assert "client abort" in logged[0]


def test_write_http_body_reraises_other_oserror():
    class Boom(io.BytesIO):
        def write(self, _body):
            raise OSError("disk full")

    try:
        write_http_body(Boom(), b"x")
    except OSError as exc:
        assert "disk full" in str(exc)
    else:
        raise AssertionError("expected OSError")
