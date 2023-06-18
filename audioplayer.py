from pygame import mixer
import os


class AudioPlayer:
    """Class used to represent an audio player.

    It is used to play songs and sounds, as well as to count the time elapsed since the beginning of the song.
    You can also adjust the playback settings.

    Methods
    -------
    on_execute(frequency=44100, size=16, channels=2, buffer=4096, volume=0.1)
        Used to set playback parameters and initialize the audio player.
    change_volume(song_volume)
        Used to set the playback volume.
    play_song()
        Used for playing music.
    update()
        Used to update the playback timer.
    """

    def __init__(self, song_bpm: float, song_source: str) -> None:
        """
        Parameters
        ----------
        song_bpm : float
            BPM of the song to be played.
        song_source : str
            Song file location.
        """
        self.mixer = mixer
        self.hitSound = self.mixer.Sound(os.path.join("src", "hitsounds", "hit.wav"))
        self.song_bpm = song_bpm
        self.songPosition = 0
        self.song_source = song_source
        self.mixer.music.load(self.song_source)

    def on_execute(self, frequency=44100, size=16, channels=2, buffer=4096, volume=0.1):
        """Used to set playback parameters and initialize the audio player.

        If no parameters are passed, the default settings are used.

        Parameters
        ----------
        frequency : int
            Audio file playback frequency.
        size : int
            Number of bits to represent audio data.
        channels : int
            Number of audio channels
        buffer : int
            Buffer size (in bytes)
        volume : int
            Playback volume.
        """
        self.mixer.pre_init(
            frequency=frequency, size=size, channels=channels, buffer=buffer
        )
        self.mixer.init()
        self.change_volume(volume)

    def change_volume(self, song_volume: float):
        """Used to set the playback volume.

        Parameters
        ----------
        song_volume : int
            Playback volume.
        Raises
        ----------
        AssertionError
            The song volume is not float.
        ValueError
            The width or height value is less than zero.
        """
        assert isinstance(song_volume, float) or isinstance(
            song_volume, int
        ), "Song volume must be float or int (0 or 1)."
        if song_volume < 0 or song_volume > 1:
            raise ValueError(
                "The volume of the song must be greater than zero and less than 1."
            )
        self.mixer.music.set_volume(song_volume)

    def play_song(self):
        """Used for playing music."""
        self.mixer.music.play()

    def update(self):
        """Used to update the playback timer."""
        self.songPosition = self.mixer.music.get_pos() + 800
