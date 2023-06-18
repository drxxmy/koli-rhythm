import pygame as pg
from pygame.locals import *
import text
import os
import enums


class UserInterface:
    """A class representing user interface.

    Methods
    -------
    update_text(score, last_grade, combo, accuracy, fps)
        Used to update UI text.
    draw()
        Used to draw UI on screen.
    """

    def __init__(
        self, score: int, last_grade: str, combo: int, accuracy: float, fps: int
    ) -> None:
        """Parameters
        ----------
        score : int
            Current score.
        last_grade : str
            Last grade.
        combo : int
            Current combo.
        accuracy : float
            Current accuracy.
        fps : int
            Current fps.

        Raises
        ------
        AssertionError
            score is not an integer.
        AssertionError
            last_grade is not a string.
        AssertionError
            combo is not an integer.
        AssertionError
            accuracy is not a float or an integer.
        AssertionError
            fps is not an integer.
        """
        assert isinstance(score, int), "score must be an integer."
        assert isinstance(last_grade, str), "last_grade must be a string."
        assert isinstance(combo, int), "combo must be an integer."
        assert isinstance(accuracy, float) or isinstance(
            accuracy, int
        ), "accuracy must be a float or an integer."
        assert isinstance(fps, int), "fps must be an integer."
        self.font = pg.font.Font(os.path.join("fonts", "PixeloidSansBold.ttf"), 45)
        self.score = text.TextWithShadow(
            f"{score:,d}",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.lastGrade = text.TextWithShadow(
            last_grade,
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.combo = text.TextWithShadow(
            str(combo),
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.accuracy = text.TextWithShadow(
            f"{round(accuracy, 2)}%",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.fps = text.TextWithShadow(
            str(int(fps)),
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )

    def update_text(
        self, score: int, last_grade: str, combo: int, accuracy: float, fps: int
    ) -> None:
        """Used to update UI text.

        Parameters
        ----------
        score : int
            Current score.
        last_grade : str
            Last grade.
        combo : int
            Current combo.
        accuracy : float
            Current accuracy.
        fps : int
            Current fps.

        Raises
        ------
        AssertionError
            score is not an integer.
        AssertionError
            last_grade is not a string.
        AssertionError
            combo is not an integer.
        AssertionError
            accuracy is not a float or an integer.
        AssertionError
            fps is not an integer.
        """
        assert isinstance(score, int), "score must be an integer."
        assert isinstance(last_grade, str), "last_grade must be a string."
        assert isinstance(combo, int), "combo must be an integer."
        assert isinstance(accuracy, float) or isinstance(
            accuracy, int
        ), "accuracy must be a float or an integer."
        assert isinstance(fps, int), "fps must be an integer."
        self.score = text.TextWithShadow(
            f"{score:,d}",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.lastGrade = text.TextWithShadow(
            last_grade,
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.combo = text.TextWithShadow(
            str(combo),
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.accuracy = text.TextWithShadow(
            f"{round(accuracy, 2)}%",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        self.fps = text.TextWithShadow(
            str(int(fps)),
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )

    def draw(self, surface: pg.surface.Surface) -> None:
        """Used to draw UI on screen.

        Parameters
        ----------
        surface : pg.surface.Surface
            Display surface.
        """
        self.score.draw(surface.get_width() - self.score.get_width(), 0, surface)
        self.lastGrade.draw(
            surface.get_width() / 2 - self.lastGrade.get_width() / 2,
            300,
            surface,
        )
        self.combo.draw(
            surface.get_width() / 2 - self.combo.get_width() / 2,
            200,
            surface,
        )
        self.accuracy.draw(
            surface.get_width() - self.accuracy.get_width(),
            self.score.get_height(),
            surface,
        )
        self.fps.draw(
            surface.get_width() - self.fps.get_width(),
            surface.get_height() - self.fps.get_height(),
            surface,
        )
