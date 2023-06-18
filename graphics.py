import os
import pygame as pg
import text
import enums
from pygame.locals import *


class Background(pg.sprite.Sprite):
    """The class that represents the background."""

    def __init__(self, image_location: str):
        """
        Parameters
        ----------
        image_location : str
            The location of the background in the file system.
        """
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_location).convert()
        self.rect = self.image.get_rect()


class Note(pg.sprite.Sprite):
    """A class that represents a game note.

    Methods
    -------
    update_vertical_position(progress)
        Used to update the vertical position of a note in relation to the calculated note progress.
    draw(screen)
        Used to draw note on screen.
    """

    def __init__(
        self,
        line: int,
        image: pg.surface.Surface,
        timing: int,
        display_surf: pg.surface.Surface,
    ) -> None:
        """
        Parameters
        ----------
        line : int
            The line number to which the note belongs.
        image : pg.surface.Surface
            An image representing a note.
        timing : int
            Timing of the note.
        display_surf : pg.surface.Surface
            Display surface.

        Raises
        ------
        AssertionError
            line is not an integer.
        AssertionError
            image is not an instance of pg.surface.Surface class.
        AssertionError
            timing is not an integer.
        AssertionError
            display_surf is not an instance of pg.surface.Surface class.
        """
        assert isinstance(line, int), "line must be an integer."
        assert isinstance(
            image, pg.surface.Surface
        ), "image must be an instance of pg.surface.Surface class."
        assert isinstance(timing, int), "timing must be an integer."
        assert isinstance(
            display_surf, pg.surface.Surface
        ), "display_surf must be an instance of pg.surface.Surface class."

        pg.sprite.Sprite.__init__(self)
        self.screen = display_surf
        self.image = image
        self.start_position = 0
        self.perfect_hit_position = self.screen.get_height() - 170
        self.timing = timing
        self.line = line
        self.offset_left = self.screen.get_width() / 2 - 258
        self.notes_margin = 132
        self.is_clickable = False
        self.rect = self.image.get_rect()
        self.rect.x = self.offset_left + (self.line - 1) * self.notes_margin
        self.rect.y = -140

    def update_vertical_position(self, progress: float) -> None:
        """Used to update the vertical position of a note in relation to the calculated note progress.

        Parameters
        ----------
        progress : float
            Calculated note progress.

        Raises
        ------
        AssertionError
            progress is not a float.
        """
        assert isinstance(progress, float), "progress must be a float."
        self.rect.y = -(
            self.start_position
            + ((self.start_position - self.perfect_hit_position) * progress)
        )

    def draw(self, screen: pg.surface.Surface) -> None:
        """Used to draw note on screen.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.

        Raises
        ------
        AssertionError
            screen is not an instance of pg.surface.Surface class.
        """
        assert isinstance(
            screen, pg.surface.Surface
        ), "screen must be an instance of pg.surface.Surface class."
        screen.blit(
            self.image,
            (
                self.rect.x,
                self.rect.y,
            ),
        )


class ButtonBar(pg.sprite.Sprite):
    """A class that represents a button bar.

    Methods
    -------
    draw(screen)
        Used to draw button bar on screen.
    """

    def __init__(self) -> None:
        self.font = pg.font.Font(os.path.join("fonts", "PixeloidSansBold.ttf"), 35)
        self.image = pg.image.load(os.path.join("sprites", "notes", "barSheet.png"))
        self.keys = ["D", "F", "J", "K"]
        self.rect = self.image.get_rect()

    def draw(self, screen: pg.surface.Surface) -> None:
        """Used to draw button bar on screen.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.

        Raises
        ------
        AssertionError
            screen is not an instance of pg.surface.Surface class.
        """
        assert isinstance(
            screen, pg.surface.Surface
        ), "screen must be an instance of pg.surface.Surface class."
        offset_left = screen.get_width() / 2 - 258
        margin = 132
        line = 0
        for key in self.keys:
            line += 1
            x = offset_left + (line - 1) * margin
            surf = pg.Surface((120, 120), SRCALPHA)
            surface = text.Text(key, self.font, (220, 220, 220))
            surface.draw(
                surf.get_width() / 2 - surface.get_width() / 2,
                surf.get_height() / 2 - surface.get_height() / 2,
                surf,
            )
            screen.blit(surf, (x, screen.get_height() - 170))

        screen.blit(
            self.image,
            (
                screen.get_width() / 2 - self.image.get_width() / 2,
                screen.get_height() - 170,
            ),
        )


class Hit:
    """A class that represents a hit.

    Methods
    -------
    get_correct_color()
        Used to get the correct color based on progress.
    get_offset()
        Used to get an offset based on progress.
    ready_to_delete()
        Used to determine if a hit is ready to be removed.
    update()
        Used to update the transparency of the hit.
    draw(screen)
        Used to draw hitbar on screen.
    """

    def __init__(self, progress: float) -> None:
        """
        Parameters
        ----------
        progress : float
            Destroyed note's progress.

        Raises
        ------
        AssertionError
            progress is not a float.
        """
        assert isinstance(progress, float), "progress must be a float."

        self.surface = pg.Surface((4, 18), SRCALPHA)
        self.progress = progress
        self.time = pg.time.get_ticks()
        self.delay = 30  # ms
        self.perfect_color = list(enums.Color.PERFECT.value)
        self.good_color = list(enums.Color.GOOD.value)
        self.bad_color = list(enums.Color.BAD.value)
        self.miss_color = list(enums.Color.MISS.value)
        self.color = self.get_correct_color()

    def get_correct_color(self) -> tuple:
        """Used to get the correct color based on progress.

        Returns
        ----------
        tuple
            Correct color.
        """
        if (
            self.progress >= 0.7
            and self.progress < 0.8
            or self.progress > 1.2
            and self.progress <= 1.3
        ):
            return self.bad_color
        elif (
            self.progress >= 0.8
            and self.progress < 0.9
            or self.progress > 1.1
            and self.progress <= 1.2
        ):
            return self.good_color
        elif self.progress >= 0.9 and self.progress <= 1.1:
            return self.perfect_color
        else:
            return self.miss_color

    def get_offset(self) -> float:
        """Used to get an offset based on progress.

        Returns
        ----------
        float
            Offset of the hit.
        """
        offset = ((self.progress - 1) * 3.33) * 98
        if offset >= 98:
            offset = 98
        elif offset <= -98:
            offset = -98
        return offset

    def ready_to_delete(self) -> bool:
        """Used to determine if a hit is ready to be removed.

        Returns
        ----------
        bool
            Is ready to be removed.
        """
        if self.color[3] == 0:
            return True
        else:
            return False

    def update(self) -> None:
        """Used to update the transparency of the hit."""
        now = pg.time.get_ticks()
        if now > self.time + self.delay:
            if self.color[3] > 0:
                self.color[3] -= 17
            self.time = now

    def draw(self, screen: pg.surface.Surface) -> None:
        """Used to draw hit on screen.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.
        Raises
        ------
        AssertionError
            screen is not an instance of pg.surface.Surface class.
        """
        assert isinstance(
            screen, pg.surface.Surface
        ), "screen must be an instance of pg.surface.Surface class."
        self.surface.fill(self.color)
        screen.blit(
            self.surface,
            (
                screen.get_width() / 2
                - self.surface.get_width() / 2
                + self.get_offset(),
                392 + self.surface.get_height() / 2,
            ),
        )


class Hitbar:
    """A class that represents a hitbar.

    Methods
    -------
    draw(screen)
        Used to draw hitbar on screen.
    """

    def __init__(self) -> None:
        self.surface = pg.Surface((200, 20), pg.SRCALPHA)
        self.hitbar_surf = pg.Surface((200, 4))
        self.hitbar_surf.fill((160, 160, 160))
        self.hitbar_center_surf = pg.Surface((4, 18))
        self.hitbar_center_surf.fill((180, 180, 180))
        self.surface.blit(
            self.hitbar_surf,
            (0, self.surface.get_height() / 2 - self.hitbar_surf.get_height() / 2),
        )
        self.surface.blit(
            self.hitbar_center_surf,
            (
                self.surface.get_width() / 2 - self.hitbar_center_surf.get_width() / 2,
                self.surface.get_height() / 2
                - self.hitbar_center_surf.get_height() / 2,
            ),
        )

    def draw(self, screen) -> None:
        """Used to draw hitbar on screen.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.

        Raises
        ------
        AssertionError
            screen is not an instance of pg.surface.Surface class.
        """
        assert isinstance(
            screen, pg.surface.Surface
        ), "screen must be an instance of pg.surface.Surface class."
        screen.blit(
            self.surface,
            (screen.get_width() / 2 - self.surface.get_width() / 2, 400),
        )
