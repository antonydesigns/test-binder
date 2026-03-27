from standard import *
from setup import Setup
from market import Market
from chart import chart

s = Setup()

inflexible_units = [
    s.units(1, "modular_reactor", 150, 200, i, 0, 20, 24, False, 0) for i in range(40)
]

s.setup_generator_bids(inflexible_units)
mo = Market(s.original_bids, s.load_schedule.iloc[: 24 * 7])
mo.start()
chart(mo.logs)
