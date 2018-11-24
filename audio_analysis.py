import librosa
import typing
import numpy
import os


class WavFile(object):

    def __init__(self, file_path):
        self.file_name = file_path
        self.amplitudes, self.frequency = librosa.load(file_path)
        self.counter = 0

    def get_splitted_audio(self, length_part=None) -> typing.Iterator[numpy.array]:
        if length_part:
            part_of_ampl = self.amplitudes[self.counter:length_part]
            self.counter = length_part
        else:
            part_of_ampl = self.amplitudes[self.counter:self.frequency]
            self.counter += self.frequency
        yield part_of_ampl

    def get_beat_rate(self):
        return self.frequency

    def get_duration_file(self):
        duration = librosa.get_duration(self.amplitudes)
        return duration


