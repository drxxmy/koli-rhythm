import json
import os


class Difficulty:
    """A class used to represent a difficulty.

    On initialization, it retrieves difficulty data from a JSON file.
    All data is stored in object attributes and can be used by other classes.

    Methods
    -------
    get_difficulty_data(json_location)
        Gets difficulty data from a JSON file.
    """

    def __init__(self, json_name: str) -> None:
        """
        Parameters
        ----------
        json_location : str
            The path of the json
        """
        self.map_directory = os.path.join(os.path.dirname(__file__), "src", "charts")
        self.json_location = os.path.join(
            os.path.dirname(__file__), "src", "charts", json_name
        )
        self.get_difficulty_data(self.json_location)

    def get_difficulty_data(self, json_location: str):
        """Gets difficulty data from a JSON file.

        Parameters
        ----------
        json_location : str
            The path of the json

        Raises
        ------
        FileNotFoundError
            If there is no JSON file in the directory.
        """
        try:
            with open(json_location, "r") as read_difficulty:
                data = json.load(read_difficulty)
                self.title = data["metadata"]["title"]
                self.artist = data["metadata"]["artist"]
                self.mapper = data["metadata"]["mapper"]
                self.bpm = float(data["metadata"]["bpm"])
                self.difficulty = data["metadata"]["difficulty"]
                self.notes = data["notes"]
                self.audio = os.path.join(data["general"]["audio"])
                self.background = data["general"]["background"]
        except FileNotFoundError as error:
            print(f"Caught {type(error)}: error")


class Chart:
    """A class used to represent a map.

    On initialization, it retrieves map data from a JSON file.
    All data is stored in object attributes and can be used by other classes.

    Methods
    -------
    """

    def __init__(self, chart_name: str) -> None:
        """
        Parameters
        ----------
        map_name : str
            The name of the map
        """
        self.map_absolute_path = os.path.join(
            os.path.dirname(__file__), "src", "charts", chart_name
        )
        self.difficulties = self.get_all_difficulties()
        self.title = self.difficulties[0].title
        self.artist = self.difficulties[0].artist
        self.mapper = self.difficulties[0].mapper
        self.bpm = self.difficulties[0].bpm
        self.audio = os.path.join(self.map_absolute_path, self.difficulties[0].audio)
        self.background = os.path.join(
            self.map_absolute_path, self.difficulties[0].background
        )

    def get_all_json_files(self):
        """Searches for a JSON files in a map directory.

        Raises
        ------
        FileNotFoundError
            If there are no JSON files in the directory.
        """
        try:
            json_files = []
            for _file in os.listdir(self.map_absolute_path):
                if _file.endswith(".json"):
                    json_files.append(_file)
            return json_files
        except FileNotFoundError as error:
            print(f"Caught {type(error)}: error")

    def get_all_difficulties(self):
        json_files = self.get_all_json_files()
        difficulties = []
        for filename in json_files:
            path = os.path.join(self.map_absolute_path, filename)
            difficulty = Difficulty(path)
            difficulties.append(difficulty)
        return difficulties


if __name__ == "__main__":
    diff = Chart("Freedom Dive")
    for name in diff.difficulties:
        print(name.difficulty)
