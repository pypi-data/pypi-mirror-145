import fameio.source.scenario as fameio


class GeneralProperties(fameio.GeneralProperties):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def make_default(cls) -> "GeneralProperties":
        default_values = {
            "RunId": 1,
            "Simulation": {
                "StartTime": "2011-12-31_23:58:00",
                "StopTime": "2012-12-30_23:58:00",
                "RandomSeed": 1,
            },
            "Output": {
                "Interval": 100,
                "Process": 0,
            },
        }
        return super().from_dict(default_values)

    def set_simulation_start_time(self, value: int) -> None:
        self._simulation_start_time = value

    def set_simulation_stop_time(self, value: int):
        self._simulation_stop_time = value

    def set_simulation_random_seed(self, value: int):
        self._simulation_random_seed = value

    def set_output_interval(self, value: int):
        self._output_interval = value

    def set_output_process(self, value: int):
        self._output_process = value
