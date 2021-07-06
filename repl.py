import sys
from buffered_stream import BufferedStream
from scheme_read import scheme_read
from eval_apply import meval
from scheme_env import the_global_environment


def driver_loop():
    while True:
        try:
            print('\n]=> ', end='', flush=True)
            result = meval(scheme_read(BufferedStream(sys.stdin)),
                           the_global_environment)
            print(';==>', result)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    driver_loop()