import pygame as pg


class SpriteSheet:
    """Class for working with spritesheet.

    Methods
    -------
    get_image(frame, width, height, scale, color)
        Used to get an image surface from the spritesheet with the given parameters.
    """

    def __init__(self, image_location: str) -> None:
        """Parameters
        ----------
        image_location : str
            Location of the spritesheet.

        Raises
        ------
        AssertionError
            image_location is not a string.
        """
        assert isinstance(image_location, str), "image_location must be a string."
        self.sheet = pg.image.load(image_location)

    def get_image(
        self, frame: int, width: int, height: int, scale: float, color: tuple
    ) -> pg.surface.Surface:
        """Used to get an image surface from the spritesheet with the given parameters.

        Parameters
        ----------
        frame : int
            Frame sequence number.
        width : int
            Width of sprite.
        height : int
            Height of sprite.
        scale : float
            Scale of the final image surface.
        color : tuple
            Key color for creating transparency.

        Returns
        ----------
        pg.surface.Surface
            Image surface.

        Raises
        ------
        AssertionError
            frame is not an integer.
        AssertionError
            width is not an integer.
        AssertionError
            height is not an integer.
        AssertionError
            scale is not a float or an integer.
        AssertionError
            color is not a tuple.
        """
        assert isinstance(frame, int), "frame must be an integer."
        assert isinstance(width, int), "width must be an integer."
        assert isinstance(height, int), "height must be an integer."
        assert isinstance(scale, float) or isinstance(
            scale, int
        ), "scale must be a float or an integer."
        assert isinstance(color, tuple), "color must be a tuple."
        img = pg.Surface((width, height)).convert_alpha()
        img.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        img = pg.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(color)
        return img
