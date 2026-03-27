from standard import *

# rng = np.random.RandomState(seed=24)
rng = np.random


class Consumer:
    def __init__(
        self,
        archetype_profile,
        shift_worker_ratio=(84, 6, 4),
        # base_load_filler_params=(300, 100, 0, 600),
        base_load_filler_params=(100, 10, 0, 300),
    ):

        self.shift_worker_ratio = shift_worker_ratio
        self.base_load_filler_params = base_load_filler_params
        self.unique_profile = self.__build_unique_profile(archetype_profile)

    def __build_unique_profile(self, archetype_profile):

        unique_profile = np.zeros(24)

        for t_from, t_to, mean, std, min, max in archetype_profile:

            load = np.clip(rng.normal(mean, std), min, max)

            for i in range(t_from, t_to):
                unique_profile[i] = load

        unique_profile = np.roll(unique_profile, self.__assign_shift_work_offset())

        return unique_profile

    def __assign_shift_work_offset(self):

        day_worker, evening_worker, night_worker = self.shift_worker_ratio
        total = day_worker + evening_worker + night_worker
        p_day = day_worker / total
        p_evening = evening_worker / total

        n = rng.rand()
        if n < p_day:
            return 0
        elif n < p_day + p_evening:
            return 8
        else:
            return -8

    def create_load_schedules(self, n_schedule=1, min=0.9, max=1.1, var=10):

        self.load_schedules = []

        for i in range(n_schedule):
            schedule = np.zeros(24)

            for i, load in enumerate(self.unique_profile):

                if load != 0:
                    schedule[i] = np.clip(rng.normal(load, var), load * min, load * max)

                elif load == 0:
                    mean, std, min, max = self.base_load_filler_params
                    schedule[i] = np.clip(rng.normal(mean, std), min, max)

            # schedule = np.roll(schedule, int(rng.normal(0, 1)))
            schedule = np.roll(schedule, int(rng.normal(0, 3)))

            self.load_schedules.append(schedule)
