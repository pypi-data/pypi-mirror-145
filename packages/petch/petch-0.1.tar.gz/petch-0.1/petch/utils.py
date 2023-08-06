from functools import reduce
import os


def linux_beep(duration:float=0.1,frequency:int=300):
    os.system(f"play -nq -t alsa synth {duration} sine {frequency}")

def compose(*func):
    def compose_function(f, g):
        return lambda *args : g(f(*args))
    return reduce(compose_function, func)