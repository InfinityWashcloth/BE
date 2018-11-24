import librosa
import typing
import numpy


class WavFile(object):

    def __init__(self, file_path, offset=0.0, duration=30):
        self.file_path = file_path
        self.offset = offset
        self.duration = duration

    def load_file(self):
        try:
            self.amplitudes, self.frequency = librosa.load(self.file_path,
                                                           offset=self.offset,
                                                           duration=self.duration)
            self.offset += self.duration
            if len(self.amplitudes):
                return True
            else:
                return False
        except KeyboardInterrupt:
            return False

    def get_splitted_audio(self) -> numpy.array:
        while self.load_file():
            return self.amplitudes

    def get_average_amplitude(self) -> float:
        while self.load_file():
            return numpy.average(self.amplitudes)

    def get_beat_rate(self):
        return self.frequency

    def get_duration_file(self):
        duration = librosa.get_duration(self.amplitudes)
        return duration
