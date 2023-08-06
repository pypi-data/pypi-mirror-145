from typing import Type
from tqdm import tqdm
from metarchive.algebra.acquisition import CallbackArguments, AcquisitionCallback


def create_acquisition_monitor(
    bar_type: Type[tqdm] = tqdm
) -> AcquisitionCallback:
    bars: dict[Type[AcquisitionCallback], bar_type] = dict(
        (arg, bar_type(desc=arg.__name__, position=i))
        for (i, arg) in enumerate(CallbackArguments.__args__)
    )

    def callback(value: CallbackArguments) -> None:
        bars[type(value)].update()

    return callback
