import pandas as pd
from solar import Solar_PowerProducer
from weather import Weather


def setup_solar_bids(capacity):
    s = Solar_PowerProducer(capacity)
    s.create_supply_schedules(9 + 7 * 4)
    w = Weather([0.5, 1.0, 2])
    w.create_schedules(9 + 7 * 4, True)
    f = w.weather_factor_schedules
    s.apply_weather_factor(f)

    solar_df = pd.DataFrame()
    for sch, schedule in enumerate(s.supply_schedules):
        for h, supply in enumerate(schedule):
            solar_df = pd.concat(
                [
                    solar_df,
                    pd.DataFrame(
                        {
                            "schedule": [sch],
                            "hour": [h],
                            "id": [1001],
                            "p_max": [supply],
                            "p_min": [0],
                            "mc": [0],
                            "sc": [0],
                            "lock_time": [0],
                            "ramp_hour": [supply],
                            "online": [False],
                            "locked": [0],
                            "prev_dispatch": [0],
                            "max_cap": [supply],
                            "min_cap": [0],
                            "type": ["solar"],
                            "dispatch": [0],
                        }
                    ),
                ]
            )
    solar_df = solar_df[solar_df["p_max"] > 0].copy()
    return solar_df


def setup_wind_bids(capacity):
    wind_capacity = capacity
    w = Weather([0.1 * wind_capacity, wind_capacity, 3])
    w.create_schedules(9 + 7 * 4, True)
    f = w.weather_factor_schedules

    wind_df = pd.DataFrame()
    for sch, schedule in enumerate(f):
        for h, supply in enumerate(schedule):
            wind_df = pd.concat(
                [
                    wind_df,
                    pd.DataFrame(
                        {
                            "schedule": [sch],
                            "hour": [h],
                            "id": [1002],
                            "p_max": [supply],
                            "p_min": [0],
                            "mc": [1],
                            "sc": [0],
                            "lock_time": [0],
                            "ramp_hour": [supply],
                            "online": [False],
                            "locked": [0],
                            "prev_dispatch": [0],
                            "max_cap": [supply],
                            "min_cap": [0],
                            "type": ["wind"],
                            "dispatch": [0],
                        }
                    ),
                ]
            )
    wind_df = wind_df[wind_df["p_max"] > 0].copy()
    return wind_df
