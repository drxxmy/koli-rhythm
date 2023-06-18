import json


class Converter:
    """The class used to convert the osu! map to a Koli Rhythm compatible file.

    Methods
    -------
    open_file(file_path)
        Used to open an osu file.
    generate_json()
        Creates JSON file with map data.
    parse_general()
        Retrieves data from the General section.
    parse_metadata()
        Retrieves data from the Metadata section.
    parse_notes()
        Retrieves data from the Objects section.
    """

    def __init__(
        self, path_to_osu: str, song_bpm: str, difficulty_name: str, rating: str
    ) -> None:
        """
        Parameters
        ----------
        path_to_osu : str
            Osu file path.
        song_bpm : str
            BPM of the song.
        difficulty_name : str
            Song difficulty name.
        rating : str
            Difficulty rating value.

        Raises
        ------
        AssertionError
            file_path, song_bpm, difficulty_name or rating is not string.
        """
        assert isinstance(path_to_osu, str), "file_path must be str."
        assert isinstance(song_bpm, str), "song_bpm must be str."
        assert isinstance(difficulty_name, str), "difficulty_name must be str."
        assert isinstance(rating, str), "rating must be str."
        self.path_to_osu = path_to_osu
        self.song_bpm = song_bpm
        self.difficulty_name = difficulty_name
        self.rating = rating
        self.map = self.open_file(path_to_osu)

    def open_file(self, file_path: str):
        """Used to open an osu file.

        Parameters
        ----------
        file_path : str
            The path to the osu file.

        Raises
        ------
        OSError
            If there are no JSON files in the directory.
        AssertionError
            file_path is not string.
        """
        assert isinstance(file_path, str), "file_path must be str."
        try:
            map_file = open(file_path, "r", encoding="utf-8")
            return map_file
        except OSError as error:
            print(f"{error}")

    def generate_json(self) -> None:
        """Used to generate a JSON file with map data."""
        general = self.parse_general()
        metadata = self.parse_metadata()
        notes = self.parse_notes()
        metadata["bpm"] = self.song_bpm
        metadata["difficulty"] = self.difficulty_name
        metadata["rating"] = self.rating
        file_name = f"{metadata['artist']} - {metadata['title']} [{metadata['difficulty']}].json"
        map_json = {"general": general, "metadata": metadata, "notes": notes}
        try:
            with open(file_name, "w") as write_file:
                json.dump(map_json, write_file)
        except FileExistsError as error:
            print("Unable to create file.")
            print(f"Caught {error}: error")

    def parse_general(self) -> dict:
        """Used to parse data from the general section of the osu file.

        Returns
        ----------
        dict
            Dictionary with general data of the map.
        """
        self.map.seek(0)
        read_from_here = False
        lines = self.map.readlines()
        general = dict()
        for line in lines:
            if line == "[General]\n":
                read_from_here = True
                continue
            if read_from_here:
                if line == "\n":
                    read_from_here = False
                data = line.split(":")
                data = [data[0], data[-1].replace("\n", "")]
                if data[0] == "AudioFile_name":
                    general["audio"] = data[1].replace(" ", "")
                data = line.split('"')
        read_from_here = False
        for line in lines:
            if line == "//Background and Video events\n":
                read_from_here = True
                continue
            if read_from_here:
                data = line.split('"')
                general["background"] = data[1].replace(" ", "")
                break
        return general

    def parse_metadata(self) -> dict:
        """Used to parse data from the metadata section of the osu file.

        Returns
        ----------
        dict
            Dictionary with metadata of the map.
        """
        self.map.seek(0)
        read_from_here = False
        lines = self.map.readlines()
        metadata = dict()
        for line in lines:
            if line == "[Metadata]\n":
                read_from_here = True
                continue
            if read_from_here:
                if line == "\n":
                    break
                data = line.split(":")
                data = [data[0], data[1].replace("\n", "")]
                if data[0] == "Title":
                    metadata["title"] = data[1]
                elif data[0] == "Artist":
                    metadata["artist"] = data[1]
                elif data[0] == "Creator":
                    metadata["mapper"] = data[1]
        return metadata

    def parse_notes(self) -> dict:
        """Used to parse data from the object section of the osu file.

        Returns
        ----------
        dict
            Dictionary with note timings and spawn positions.
        """
        self.map.seek(0)
        read_from_here = False
        lines = self.map.readlines()
        notes = dict()
        for line in lines:
            if line == "[HitObjects]\n":
                read_from_here = True
                continue
            if read_from_here:
                colomn = line.split(",")[:1:]
                colomn = "".join(map(str, colomn))
                timing = line.split(",")[2:3:]
                timing = int("".join(map(str, timing)))
                if timing not in notes:
                    spawn_positions = "0000"
                    spawn_positions = list(spawn_positions)
                    if colomn == "64":
                        spawn_positions[0] = "1"
                    if colomn == "192":
                        spawn_positions[1] = "1"
                    if colomn == "320":
                        spawn_positions[2] = "1"
                    if colomn == "448":
                        spawn_positions[3] = "1"
                    spawn_positions = "".join(spawn_positions)
                    notes[timing] = spawn_positions
                else:
                    spawn_positions = list(notes[timing])
                    if colomn == "64":
                        spawn_positions[0] = "1"
                    if colomn == "192":
                        spawn_positions[1] = "1"
                    if colomn == "320":
                        spawn_positions[2] = "1"
                    if colomn == "448":
                        spawn_positions[3] = "1"
                    notes[timing] = "".join(spawn_positions)
        return notes
