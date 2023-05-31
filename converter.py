import json


class Converter:
    """The class used to convert the osu! map to a Koli Rhythm compatible file.

    Methods
    -------
    openFile(filePath)
        Used to open an osu file.
    generateJson()
        Creates JSON file with map data.
    parseGeneral()
        Retrieves data from the General section.
    parseMetadata()
        Retrieves data from the Metadata section.
    parseNotes()
        Retrieves data from the Objects section.
    """

    def __init__(
        self, pathToOsu: str, songBpm: str, difficultyName: str, rating: str
    ) -> None:
        """
        Parameters
        ----------
        pathToOsu : str
            Osu file path.
        songBpm : str
            BPM of the song.
        difficultyName : str
            Song difficulty name.
        rating : str
            Difficulty rating value.
        """
        self.pathToOsu = pathToOsu
        self.songBpm = songBpm
        self.difficultyName = difficultyName
        self.rating = rating
        self.map = self.openFile(pathToOsu)

    def openFile(self, filePath: str):
        """Used to open an osu file.

        Parameters
        ----------
        filePath : str
            The path to the osu file.

        Raises
        ------
        OSError
            If there are no JSON files in the directory.
        """
        try:
            mapFile = open(filePath, "r", encoding="utf-8")
            return mapFile
        except OSError as error:
            print(f"{error}")

    def generateJson(self) -> None:
        """Used to generate a JSON file with map data."""
        general = self.parseGeneral()
        metadata = self.parseMetadata()
        notes = self.parseNotes()
        metadata["bpm"] = self.songBpm
        metadata["difficulty"] = self.difficultyName
        metadata["rating"] = self.rating
        fileName = f"{metadata['artist']} - {metadata['title']} [{metadata['difficulty']}].json"
        map_json = {"general": general, "metadata": metadata, "notes": notes}
        try:
            with open(fileName, "w") as write_file:
                json.dump(map_json, write_file)
        except FileExistsError as error:
            print("Unable to create file.")
            print(f"Caught {error}: error")

    def parseGeneral(self) -> dict:
        """Used to parse data from the general section of the osu file."""
        self.map.seek(0)
        readfromhere = False
        lines = self.map.readlines()
        general = dict()
        for line in lines:
            if line == "[General]\n":
                readfromhere = True
                continue
            if readfromhere:
                if line == "\n":
                    readfromhere = False
                data = line.split(":")
                data = [data[0], data[-1].replace("\n", "")]
                if data[0] == "AudioFilename":
                    general["audio"] = data[1].replace(" ", "")
                data = line.split('"')
        readfromhere = False
        for line in lines:
            if line == "//Background and Video events\n":
                readfromhere = True
                continue
            if readfromhere:
                data = line.split('"')
                general["background"] = data[1].replace(" ", "")
                break
        return general

    def parseMetadata(self) -> dict:
        """Used to parse data from the metadata section of the osu file."""
        self.map.seek(0)
        readfromhere = False
        lines = self.map.readlines()
        metadata = dict()
        for line in lines:
            if line == "[Metadata]\n":
                readfromhere = True
                continue
            if readfromhere:
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

    def parseNotes(self) -> dict:
        """Used to parse data from the object section of the osu file."""
        self.map.seek(0)
        readfromhere = False
        lines = self.map.readlines()
        notes = dict()
        for line in lines:
            if line == "[HitObjects]\n":
                readfromhere = True
                continue
            if readfromhere:
                colomn = line.split(",")[:1:]
                colomn = "".join(map(str, colomn))
                timing = line.split(",")[2:3:]
                timing = int("".join(map(str, timing)))
                if timing not in notes:
                    spawnPositions = "0000"
                    spawnPositions = list(spawnPositions)
                    if colomn == "64":
                        spawnPositions[0] = "1"
                    if colomn == "192":
                        spawnPositions[1] = "1"
                    if colomn == "320":
                        spawnPositions[2] = "1"
                    if colomn == "448":
                        spawnPositions[3] = "1"
                    spawnPositions = "".join(spawnPositions)
                    notes[timing] = spawnPositions
                else:
                    spawnPositions = list(notes[timing])
                    if colomn == "64":
                        spawnPositions[0] = "1"
                    if colomn == "192":
                        spawnPositions[1] = "1"
                    if colomn == "320":
                        spawnPositions[2] = "1"
                    if colomn == "448":
                        spawnPositions[3] = "1"
                    notes[timing] = "".join(spawnPositions)
        return notes
