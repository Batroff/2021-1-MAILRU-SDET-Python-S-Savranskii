import time


def wait(method, error=Exception, timeout=10, interval=0.5, check=False, **kwargs):
    st = time.time()
    last_exception = None
    while time.time() - st < timeout:
        try:
            result = method(**kwargs)
            if check:
                if result:
                    return result
                last_exception = f'Method {method.__name__} returned {result}'
            else:
                return result
        except error as e:
            last_exception = e
        time.sleep(interval)

    raise TimeoutError(f'Method {method.__name__} timeout in {timeout}sec with exception: "{last_exception}"')
