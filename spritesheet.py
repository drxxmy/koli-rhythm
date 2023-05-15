import pygame as pg


class SpriteSheet:
    """Class for working with spritesheet.

    !!!! ADD_MORE_INFO_HERE !!!!

    Methods
    -------
    get_image(frame, width, height, scale, colour)
        Returns the image surface from the spritesheet with the given parameters
    """

    def __init__(self, imageLocation: str) -> None:
        """Parameters
        ----------
        imageLocation : str
            Location of the spritesheet.
        """
        self.sheet = pg.image.load(imageLocation)

    def get_image(
        self, frame: int, width: int, height: int, scale: float, colour: set
    ) -> pg.Surface:
        """Parameters
        ----------
        frame : int
            Frame sequence number.
        width : int
            Width of sprite.
        height : int
            Height of sprite.
        scale : float
            Scale of the final image surface.
        colour : set
            Key colour for creating transparency.
        """
        img = pg.Surface((width, height)).convert_alpha()
        img.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        img = pg.transform.scale(img, (width * scale, height * scale))
        img.set_colorkey(colour)
        return img
