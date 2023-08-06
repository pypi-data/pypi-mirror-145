import numpy as np

from pymusicbox.audio.audio_utils import add_audio

from pymusicbox.symbolic.symbols import Note, Track


class Instrument:
    def __init__(self, sample_rate=44100, harmonics=None):
        self.sample_rate = sample_rate
        self.max_amp = 9000

        self.harmonics_enabled = False

        if harmonics is not None:
            self.attack_length = harmonics['atk']
            self.decay_length = harmonics['dec']
            self.release_length = harmonics['rls']
            self.sustain_factor = harmonics['sus_factor']

            self.harmonics_enabled = True

    def get_harmonics(self, length):
        sustain_length = length - \
            (self.attack_length + self.decay_length + self.release_length)

        atk = np.linspace(0, 1, int(self.attack_length * self.sample_rate))
        dec = np.linspace(1, self.sustain_factor, int(
            self.decay_length * self.sample_rate))
        sus = np.linspace(self.sustain_factor, self.sustain_factor, int(
            sustain_length * self.sample_rate))
        rls = np.linspace(self.sustain_factor, 0, int(
            self.release_length * self.sample_rate))

        return np.concatenate([atk, dec, sus, rls])

    def render_note(self, note: Note):
        freq = 55 * pow(2, (note.note / 12))
        t = np.linspace(0, note.length, int(note.length*self.sample_rate))

        data = self.max_amp * note.level * np.sin(2. * np.pi * freq * t)
        if self.harmonics_enabled:
            data *= self.get_harmonics(note.length)

        return data

    def render_track(self, track: Track):
        data = np.zeros((int(track.length*self.sample_rate),))

        for time, note in track.get_timed_notes():
            add_audio(time, data, self.render_note(note), self.sample_rate)

        return data
