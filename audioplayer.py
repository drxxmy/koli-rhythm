from pygame import mixer
import time
import os


class AudioPlayer:
    """Class used to represent an audio player.

    It is used to play songs and sounds, as well as to count the time elapsed since the beginning of the song.
    You can also adjust the playback settings.

    Methods
    -------
    on_execute(frequency=44100, size=16, channels=2, buffer=4096, volume=0.1)
        Used to set playback parameters and initialize the audio player.
    changeVolume(songVolume)
        Used to set the playback volume.
    playSong()
        Used for playing music.
    update()
        Used to update the playback timer.
    """

    def __init__(self, songBpm: float, songSource: str) -> None:
        """
        Parameters
        ----------
        songBpm : float
            BPM of the song to be played.
        songSource : str
            Song file location.
        """
        self.mixer = mixer
        self.hitSound = self.mixer.Sound(os.path.join("src", "hitsounds", "hit.wav"))
        self.songBpm = songBpm
        self.songPosition = 0
        self.elapsedTime = round(time.time() * 1000)
        self.songSource = songSource
        self.mixer.music.load(self.songSource)

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
        self.changeVolume(volume)

    def changeVolume(self, songVolume: float):
        """Used to set the playback volume.

        Parameters
        ----------
        songVolume : int
            Playback volume.
        """
        self.mixer.music.set_volume(songVolume)

    def playSong(self):
        """Used for playing music."""
        self.mixer.music.play()

    def update(self):
        """Used to update the playback timer."""
        self.songPosition = round(time.time() * 1000) - self.elapsedTime
