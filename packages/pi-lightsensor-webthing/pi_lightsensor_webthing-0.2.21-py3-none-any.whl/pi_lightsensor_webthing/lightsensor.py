import logging
import board
import adafruit_bh1750
from threading import Thread
from time import sleep


class LightSensossh
    def __init__(self, sampling_rate_sec: int = 1, smoothing_window_sec: int = 15, refreshing_rate_sec:int=1):
        self.smoothing_window_sec = smoothing_window_sec
        self.sampling_rate_sec = sampling_rate_sec
        self.refreshing_rate_sec = refreshing_rate_sec
        self.measures = list()
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)
        logging.info("light sensor connected")

    def update_smoothing_window(self, smoothing_window_sec: int):
        self.smoothing_window_sec = smoothing_window_sec

    def update_sampling_rate(self, sampling_rate_sec: int):
        self.sampling_rate_sec = sampling_rate_sec

    def update_refreshing_rate(self, refreshing_rate_sec: int):
        self.refreshing_rate_sec = refreshing_rate_sec

    def listen(self, listener):
        Thread(target=self.__listen, args=(listener,), daemon=True).start()

    def __listen(self, listener):
        loop = 0
        while True:
            try:
                self.measures.append(self.sensor.lux)
                while len(self.measures) > self.smoothing_window_sec:
                    self.measures.pop(0)
                loop +=1
                if loop >= self.refreshing_rate_sec:
                    loop = 0
                    sorted_measures = sorted(self.measures)
                    median = sorted_measures[int(len(sorted_measures) * 0.5)]
                    listener(int(median))
            except Exception as e:
                print("error occurred", e)
            sleep(self.sampling_rate_sec)

