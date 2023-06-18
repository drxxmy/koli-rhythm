import chart
import pygame as pg
import os
from graphics import Note
import spritesheet
import enums


class Spawner:
    """The class used to represent a notes spawner.

    Methods
    -------
    get_note_images()
        Used to get all note images.
    get_spawn_lines(note_positions)
        Used to get spawn lines for certain notes positions.
    get_image_for_note(line)
        Used to image the surface relative to the spawn line.
    spawn_notes(screen)
        Used to spawn notes.
    """

    def __init__(self, difficulty: chart.Difficulty) -> None:
        """
        Parameters
        ----------
        difficulty : chart.Difficulty
            Selected difficulty.

        Raises
        ------
        AssertionError
            difficulty is not an instance of the chart.Difficulty class.
        """
        assert isinstance(
            difficulty, chart.Difficulty
        ), "difficulty must be an instance of the chart.Difficulty class."
        self.selected_difficulty = difficulty
        self.note_images = self.get_note_images()

    def get_note_images(self) -> list:
        """Used to get all note images.

        Returns
        ----------
        list
            List of all note images.
        """
        images = []
        notesSheet = spritesheet.SpriteSheet(
            os.path.join("sprites", "notes", "notesSheet.png")
        )
        for frame in range(0, 4):
            image = notesSheet.get_image(frame, 120, 120, 1, enums.Color.BLACK.value)
            images.append(image)
        return images

    def get_spawn_lines(self, note_positions: str) -> list:
        """Used to get spawn lines for certain notes positions.

        Parameters
        ----------
        note_positions : str
            Note positions.

        Returns
        ----------
        list
            List of spawn lines.
        """
        return [
            index + 1 for index, number in enumerate(note_positions) if number == "1"
        ]

    def get_image_for_note(self, line: int) -> pg.surface.Surface:
        """Used to image the surface relative to the spawn line.

        Parameters
        ----------
        line : int
            Line number.

        Returns
        ----------
        pg.surface.Surface
            Suitable image.
        """
        return self.note_images[line - 1]

    def spawn_notes(self, screen: pg.surface.Surface) -> list:
        """Used to spawn notes.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.

        Returns
        ----------
        list
            List of spawned notes.
        """
        notes = []
        for timing in self.selected_difficulty.notes:
            note_positions = self.selected_difficulty.notes[timing]
            spawn_lines = self.get_spawn_lines(note_positions)
            timing = int(int(timing) - 350 / 2)
            for line in spawn_lines:
                image = self.get_image_for_note(line)
                note = Note(
                    line=line,
                    image=image,
                    timing=timing,
                    display_surf=screen,
                )
                notes.append(note)
        return notes
