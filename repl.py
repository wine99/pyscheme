import sys
from buffered_stream import BufferedStream
from scheme_read import scheme_read
from eval_apply import meval
from scheme_env import setup_environment


def driver_loop():
    f = BufferedStream(sys.stdin)
    the_global_environment = setup_environment()
    while True:
        try:
            print('\n]=> ', end='', flush=True)
            result = meval(scheme_read(f), the_global_environment)
            print(';==>', result)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    driver_loop()
