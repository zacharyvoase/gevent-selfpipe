"""Self-pipe trick utilities for greenlet."""

from functools import wraps
import os
import sys
import threading

import gevent.socket


def selfpipe(func, *args, **kwargs):

    """
    Run a thread using the self-pipe trick for gevent synchronization.

    Runs the provided function, with arguments, in a separate thread, using
    the self-pipe trick to synchronize the completion of that thread with the
    gevent loop in the main thread. Any value returned or exception raised by
    the provided function will propagate.

    You can call this function directly to co-operatively yield while making a
    normally-blocking call, or use ``gevent.spawn()`` with it to run a
    traditional blocking function as a background greenlet.

    Note that the called function should *not* use gevent in any way (gevent
    raises an exception if used from more than one thread), and if you want
    good performance characteristics, it should probably be a GIL-releasing
    C or Cython function.
    """

    read_fd, write_fd = os.pipe()

    result_container = []

    def runner():
        try:
            result = func(*args, **kwargs)
            result_container.append((True, result))
        except Exception, exc:
            result_container.append((False,) + sys.exc_info())
        finally:
            os.write(write_fd, '\x00')

    thread = threading.Thread(target=runner)
    thread.start()

    try:
        gevent.socket.wait_read(read_fd)
        os.read(read_fd, 1)
    finally:
        thread.join()
        os.close(read_fd)
        os.close(write_fd)

    success, value = result_container[0][:2]
    if success:
        return value
    raise value


def selfpiped(function):

    """
    A decorator to declare a function as always using the self-pipe trick.

    This means the decorated function will always be run in a background thread
    with self-pipe gevent synchronization.

    An example using ZeroMQ:

        >>> import zmq
        >>> @selfpiped
        ... def device(d_type, isock, osock):
        ...     try:
        ...         zmq.device(d_type, isock, osock)
        ...     finally:
        ...         isock.close(); osock.close()
        >>> dev_gl = gevent.spawn(device, zmq.STREAMER, isock, osock)
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        return selfpipe(function, *args, **kwargs)
    return wrapper
