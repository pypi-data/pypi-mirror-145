import time
import signal
import asyncio
from functools import wraps
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool

def exec_time(logger=None):
    '''
    Decorator for module execution time.
    '''

    def timeit(f):
        @wraps(f)
        def timed(*args, **kwargs):
            ts = time.time()
            result = f(*args, **kwargs)
            te = time.time()
            if logger:
                logger.debug('[%r] execution time: %2.2f seconds' %
                             (f.__name__, (te-ts)))
            else:
                print('[%r] execution time: %2.2f seconds' %
                      (f.__name__, (te-ts)))
            return result
        return timed
    return timeit


def retry(*exceptions, retries=4, delay=4, logger=None):
    '''
    Decorator for function retry
    '''

    def deco_retry(f):
        @wraps(f)
        def inner(*args, **kwargs):
            mtries, mdelay = retries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:                    
                    msg = '%s; %d tries left, Retrying in %d seconds...' % (str(e), mtries, mdelay)
                    mtries -= 1

                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)

                    time.sleep(mdelay)

            return f(*args, **kwargs)
        inner.__name__ = f.__name__
        return inner
    return deco_retry


def async_retry(*exceptions, retries=4, delay=4, logger=None):
    '''
    Decorator for async function retry.
    '''

    def deco_retry(f):
        @wraps(f)
        async def inner(*args, **kwargs):
            mtries, mdelay = retries, delay

            while mtries > 0:
                try:
                    return await f(*args, **kwargs)
                except exceptions as e:
                    msg = '{}; {} tries left, Retrying in {} seconds...'.format(str(e), mtries, mdelay)
                    mtries -= 1

                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)

                    await asyncio.sleep(mdelay)

            return await f(*args, **kwargs)

        return inner
    return deco_retry

class DTCTimeoutException(Exception):
    def __init__(self, seconds):
        self.message = 'timeout after {} seconds'.format(seconds)
        super().__init__(self.message)

def timeout(s, handler=None):
    '''
    Timeout decorator.
    ref: https://anonbadger.wordpress.com/2018/12/15/python-signal-handlers-and-exceptions/
    param: 
        s:  time in seconds the function run before terminated.
        handler:  optional, for unix like system only, define custom function handling the timeout event.
    '''

    def deco_timeout(f):
        if hasattr(signal, "SIGALRM"):
            '''
            for unix like system.
            '''
            @wraps(f)
            def inner(*args, **kwargs):
                _handler = lambda _s, _f: (_ for _ in ()).throw(DTCTimeoutException(s)) if handler == None else handler

                signal.signal(signal.SIGALRM, _handler)
                signal.alarm(s)
                try:
                    return f(*args, **kwargs)
                except:
                    raise
                finally:
                    signal.alarm(0)
                
            return inner

        else:
            '''
            for others systems without SIGALRM, use multiprocessing instead.
            '''

            def wrapper(*args, **kwargs):
                pool = ThreadPool(processes=1)
                results = pool.apply_async(f, args, kwargs)
                pool.close()
                try:
                    return results.get(s)
                except TimeoutError:
                    raise DTCTimeoutException(s)
                finally:
                    pool.terminate() ## thread seems still running. todo...

            return wrapper

    return deco_timeout