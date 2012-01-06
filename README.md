# gevent-selfpipe

A simple hack to allow blocking calls to be made in Python background threads
but with gevent-based scheduling (so that other greenlets can run while the
call completes). It does this using the [self-pipe trick][], normally used for
avoiding race conditions in signal handling but surprisingly nifty in this
circumstance.

  [self-pipe trick]: http://cr.yp.to/docs/selfpipe.html


## Example

```pycon
>>> import time
>>> import gevent
>>> from gevent_selfpipe import selfpipe
>>> def print_something():
...     print "If this message appears it means the main thread yielded."
>>> gl = gevent.spawn(print_something)
>>> time.sleep(1) # Waits 1 second, nothing printed.
>>> selfpipe(time.sleep, 1) # Waits 1 second.
If this message appears it means the main thread yielded.
```


## Installation

    pip install gevent-selfpipe


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
