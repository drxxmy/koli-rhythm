import pygame as pg


class Text:
    """Class used to represent text for pygame.

    Methods
    -------
    get_size()
        Used to get size of the text surface.
    get_width()
        Used to get width of the text surface.
    get_height()
        Used to get height of the text surface.
    draw(x, y, surface)
        Used to draw a text with shadow on surface.
    """

    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        text_col: set,
    ) -> None:
        """
        Parameters
        ----------
        text : str
            Text to draw on screen.
        font : pg.font.Font
            Pygame font.
        text_col : set
            Text colour in RGB.
        """
        self.text = text
        self.font = font
        self.text_col = text_col
        self.text_surf = self.font.render(self.text, True, self.text_col)

    def get_size(self) -> tuple:
        """Used to get size of the text surface."""
        return self.text_surf.get_size()

    def get_width(self) -> int:
        """Used to get width of the text surface."""
        return self.text_surf.get_width()

    def get_height(self) -> int:
        """Used to get height of the text surface."""
        return self.text_surf.get_height()

    def draw(self, x: float, y: float, surface: pg.surface.Surface) -> None:
        """Used to draw a text with shadow on surface.

        Parameters
        ----------
        x : float
            X position of the text.
        y : float
            Y position of the text.
        surface : pg.surface.Surface
            Surface for drawing text.
        """
        surface.blit(self.text_surf, (x, y))


class TextWithShadow:
    """Class used to represent text with shadow for pygame.

    Methods
    -------
    get_size()
        Used to get size of the text surface.
    get_width()
        Used to get width of the text surface.
    get_height()
        Used to get height of the text surface.
    draw(x, y, surface)
        Used to draw a text with shadow on surface.
    """

    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        text_col: set,
        shadow_col: set,
        shadow_offset: float,
    ) -> None:
        """
        Parameters
        ----------
        text : str
            Text to draw on screen.
        font : pg.font.Font
            Pygame font.
        text_col : set
            Text colour in RGB.
        shadow_col : set
            Shadow colour in RGB.
        shadow_offset : float
            Offset of the shadow.
        """
        self.text = text
        self.font = font
        self.text_col = text_col
        self.shadow_col = shadow_col
        self.shadow_offset = shadow_offset
        self.text_surf = self.font.render(self.text, True, self.text_col)
        self.shadow_surf = self.font.render(self.text, True, self.shadow_col)
        self.width = self.text_surf.get_width() + self.shadow_offset
        self.height = self.text_surf.get_height() + self.shadow_offset
        self.size = (self.width, self.height)

    def get_size(self) -> tuple:
        """Used to get size of the text surface."""
        return self.size

    def get_width(self) -> int:
        """Used to get width of the text surface."""
        return self.width

    def get_height(self) -> int:
        """Used to get height of the text surface."""
        return self.height

    def draw(self, x: float, y: float, surface: pg.surface.Surface) -> None:
        """Used to draw a text with shadow on surface.

        Parameters
        ----------
        x : float
            X position of the text.
        y : float
            Y position of the text.
        surface : pg.surface.Surface
            Surface for drawing text.
        """
        surface.blit(self.shadow_surf, (x + self.shadow_offset, y + self.shadow_offset))
        surface.blit(self.text_surf, (x, y))
