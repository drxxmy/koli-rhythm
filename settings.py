import json
import os


class Settings:
    """The class used to represent a player's performance.

    Methods
    -------
    load()
        Used to load settings from a file.
    save()
        Used to save settings to a file
    load_default_settings()
        Used to load default settings.
    file_exists()
        Used to check if settings file exists.
    calculate_time_to_react()
        Used to calculate time to react on note.
    calculate_background_alpha()
        Used to calculate background dim.
    increment_note_speed()
        Used to increment note speed.
    decrement_note_speed()
        Used to decrement note speed.
    increment_background_dim()
        Used to increment background dim.
    decrement_background_dim()
        Used to decrement background dim.
    increment_volume()
        Used to increment volume.
    decrement_volume()
        Used to decrement volume.
    """

    def __init__(self) -> None:
        self.settings_path = "settings.json"
        if self.file_exists():
            self.load()
        else:
            self.load_default_settings()

    def load(self) -> None:
        """Used to load settings from a file.

        Raises
        ------
        FileNotFoundError
            File cannot be opened or doesn't exist.
        """
        try:
            with open(self.settings_path, "r") as settings_file:
                data = json.load(settings_file)
                self.username = data["username"]
                self.note_speed = round(data["note_speed"], 1)
                self.background_dim = data["background_dim"]
                self.volume = data["volume"]
        except FileNotFoundError as error:
            print(f"Caught {type(error)}: error")
        self.background_alpha = self.calculate_background_alpha()
        self.time_to_react = self.calculate_time_to_react()

    def save(self) -> None:
        """Used to save settings to a file.

        Raises
        ------
        OSError
            Unable to save file.
        """
        data = {
            "username": self.username,
            "note_speed": round(self.note_speed, 1),
            "background_dim": self.background_dim,
            "volume": self.volume,
        }
        try:
            with open(self.settings_path, "w") as settings_file:
                json.dump(data, settings_file)
        except OSError as error:
            print(f"Caught {type(error)}: error")

    def load_default_settings(self) -> None:
        """Used to load default settings."""
        self.username = ""
        self.note_speed = 1.0
        self.background_dim = 0
        self.background_alpha = self.calculate_background_alpha()
        self.volume = 100
        self.time_to_react = self.calculate_time_to_react()

    def file_exists(self) -> bool:
        """Used to check if settings file exists.

        Returns
        ----------
        bool
            The file exist.
        """
        return os.path.isfile(self.settings_path)

    def calculate_time_to_react(self) -> int:
        """Used to calculate time to react on note.

        Returns
        ----------
        int
            Time to react on note.
        """
        time_to_react = round(725 - self.note_speed * 10 * 25)
        return time_to_react

    def calculate_background_alpha(self) -> int:
        """Used to calculate background dim.

        Returns
        ----------
        int
            Background dim.
        """
        background_alpha = round(self.background_dim * 2.55)
        return background_alpha

    def increment_note_speed(self) -> None:
        """Used to increment note speed."""
        if self.time_to_react > 200:
            self.note_speed += 0.1
            self.time_to_react = self.calculate_time_to_react()

    def decrement_note_speed(self) -> None:
        """Used to decrement note speed."""
        if self.time_to_react < 600:
            self.note_speed -= 0.1
            self.time_to_react = self.calculate_time_to_react()

    def increment_background_dim(self) -> None:
        """Used to increment background dim."""
        if self.background_dim < 100:
            self.background_dim += 5
            self.background_alpha = self.calculate_background_alpha()

    def decrement_background_dim(self) -> None:
        """Used to decrement background dim."""
        if self.background_dim > 0:
            self.background_dim -= 5
            self.background_alpha = self.calculate_background_alpha()

    def increment_volume(self) -> None:
        """Used to increment volume."""
        if self.volume < 100:
            self.volume += 5

    def decrement_volume(self) -> None:
        """Used to decrement volume."""
        if self.volume > 0:
            self.volume -= 5
