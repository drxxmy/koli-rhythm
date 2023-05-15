import json
import time
import pygame as pg
import os
from pygame.locals import *


# imports
import spritesheet
import audioplayer
import converter

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Constants
FPS = 1000


class Background(pg.sprite.Sprite):
    """Class representing a background."""

    def __init__(self, imageLocation: str):
        """
        Parameters
        ----------
        imageLocation : str
            Location of the background in the file system.
        """
        pg.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pg.image.load(imageLocation).convert()

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()


class Note(pg.sprite.Sprite):
    """Class representing a game note.

    Methods
    -------
    updateimageScaling(imageScaling)
        Used to update image scaling.
    generateJson()
        Creates JSON file with map data.
    """

    def __init__(
        self, line: int, display_surf: pg.surface.Surface, imageScaling: float
    ) -> None:
        """
        Parameters
        ----------
        line : int
            Line number to which the note belongs.
        display_surf : pg.surface.Surface
            Display surface.
        imageScaling : float
            Scaling of the note sprite.
        """
        pg.sprite.Sprite.__init__(self)
        self._display_surf = display_surf
        self.imageScaling = imageScaling
        self.startPosition = 0
        self.perfectHitPosition = (
            self._display_surf.get_height() - 170 * self.imageScaling
        )
        self.timing = 0
        self.line = line
        self.OffsetLeft = self._display_surf.get_width() / 2 - (245 * self.imageScaling)
        self.MarginBetweenNotes = 132.3 * self.imageScaling

        self._x = self.OffsetLeft + (self.line - 1) * self.MarginBetweenNotes
        self.y = -140

    def updateimageScaling(self, imageScaling: float):
        """Used to update image scaling."""
        self.imageScaling = imageScaling


class SingleNote(Note):
    def __init__(self, y: int, line: int) -> None:
        super().__init__(y, line)


class LongNote(Note):
    def __init__(self, x: int, y: int, line: int, length: int) -> None:
        super().__init__(x, y, line)
        self.length = length


class Difficulty:
    def __init__(self) -> None:
        raise NotImplementedError


class Map:
    """A class used to represent a map.

    On initialization, it retrieves map data from a JSON file.
    All data is stored in object attributes and can be used by other classes.

    Methods
    -------
    searchJson(mapDirectory)
        Searches for a JSON file in a map directory.
    getMapData(mapDirectory)
        Gets map data from a JSON file.
    """

    def __init__(self, mapDirectory: str) -> None:
        """
        Parameters
        ----------
        mapDirectory : str
            The path of the map directory
        """
        self.getMapData(mapDirectory)

    def searchJson(self, mapDirectory) -> str:
        """Searches for a JSON file in a map directory.

        Parameters
        ----------
        mapDirectory : str
            The path of the map directory

        Raises
        ------
        FileNotFoundError
            If there are no JSON files in the directory.
        """
        try:
            for _file in os.listdir(mapDirectory):
                if _file.endswith(".json"):
                    return os.path.join(mapDirectory, _file)
        except FileNotFoundError as error:
            print(f"Caught {type(error)}: error")

    def getMapData(self, mapDirectory):
        """Gets map data from a JSON file.

        Parameters
        ----------
        mapDirectory : str
            The path of the map directory

        Raises
        ------
        FileNotFoundError
            If there are no JSON files in the directory.
        """
        jsonFile = self.searchJson(mapDirectory=mapDirectory)
        if jsonFile:
            try:
                with open(jsonFile, "r") as read_map:
                    data = json.load(read_map)
                    self.title = data["metadata"]["title"]
                    self.artist = data["metadata"]["artist"]
                    self.mapper = data["metadata"]["mapper"]
                    self.bpm = int(data["metadata"]["bpm"])
                    self.difficulty = data["metadata"]["difficulty"]
                    self.notes = data["notes"]
                    self.audio = f"{mapDirectory}{data['general']['audio']}"
                    self.background = os.path.join(
                        mapDirectory, data["general"]["background"]
                    )
            except FileNotFoundError as error:
                print(f"Caught {type(error)}: error")


class InputHandler:
    def __init__(self) -> None:
        raise NotImplementedError


class Game:
    """The main class that implements the logic of the game.

    !!!! ADD_MORE_INFO_HERE !!!!

    Methods
    -------
    on_init()
        Used to initialize the pygame module, game window and some variables.
    loadResources()
        Used to load resources of the game. (Fonts, sprites etc)
    spawnNotes()
        Used to spawn notes of certain map.
    drawRectangle()
        Used to draw two rectangles as a playfield.
    updateNotes()
        Used to update the position of notes relative to the audio player's timer.
    drawText(text, font, text_col, x, y)
        Used to draw a text on screen.
    drawNotes()
        Used to draw notes on screen.
    drawJudgementBar()
        Used to draw a judgement bar on screen.
    drawBG()
        Used to draw a background.
    handleInput(eventType, key)
        Used to handle keyboard input of the player.
    resizeSprites()
        Used to resize all sprites.
    waitBeforePlayingSong()
        Used to wait before playing a song.
    on_event(event)
        Used to handle pygame events.
    on_loop()
        Used to perform a game loop.
    on_render()
        Used to perform rendering on screen.
    on_cleanup()
        Used to handle cleanup when the game is closed.
    on_execute()
        Used to perform a game logic.
    """

    def __init__(self, width: int, height: int, initializationFlags) -> None:
        """
        Parameters
        ----------
        width : int
            Playback volume.
        height : int
            Playback volume.
        initializationFlags : int
            Playback volume.
        """
        self._running = True
        self._flags = initializationFlags
        self.size = self.width, self.height = width, height

    def on_init(self) -> None:
        """Used to initialize the pygame module, game window and some variables."""
        pg.init()
        pg.display.set_caption("Koli Rhythm")
        self.clock = pg.time.Clock()
        self.lowestFps = 99999
        self._display_surf = pg.display.set_mode(self.size, self._flags)

        self.imageScaling = 1
        self.pressedKeys = [False, False, False, False]
        self.map = Map("src/maps/The Lost Dedicated/")
        self.audioPlayer = audioplayer.AudioPlayer(self.map.bpm, self.map.audio)

        self.menu_text = ["Resume", "Retry", "Quit"]
        self.selected_option = 0
        self.gamePaused = False
        self.timeToReact = 350
        self.waitBeforePlaying = 1000
        self.startedPlayingSong = False
        self.all_notes = pg.sprite.Group()
        self.other_sprites = pg.sprite.RenderUpdates()
        self.loadResources()
        self.resizeSprites()

    def loadResources(self) -> None:
        """Used to load resources of the game. (Fonts, sprites etc)"""
        self.notesSheet = spritesheet.SpriteSheet(
            os.path.join("sprites", "notes", "notesSheet.png")
        )
        self.firstNote = self.notesSheet.get_image(0, 120, 120, 1, BLACK)
        self.secondNote = self.notesSheet.get_image(1, 120, 120, 1, BLACK)
        self.thirdNote = self.notesSheet.get_image(2, 120, 120, 1, BLACK)
        self.fourthNote = self.notesSheet.get_image(3, 120, 120, 1, BLACK)
        self.judgementBar = pg.image.load(
            os.path.join("sprites", "notes", "barSheet.png")
        )
        self.font = pg.font.Font(os.path.join("fonts", "PixeloidSansBold.ttf"), 45)
        self.background = Background(self.map.background)
        self.other_sprites.add(self.background)
        self._JudgementCircleSprite = pg.image.load(
            os.path.join("sprites", "ui", "JudgementCircle.png")
        ).convert_alpha()
        # self.BgSprite = self._BgSprite
        self.JudgementCircleSprite = self._JudgementCircleSprite

    def spawnNotes(self) -> None:
        """Used to spawn notes of certain map.

        It checks if the audio player timer is equal or more than note timings
        and creates a new instance of the note corresponding to the desired line
        above the screen.
        """
        for key in self.map.notes:
            if (
                self.audioPlayer.songPosition >= int(key)
                and self.map.notes[key] != None
            ):
                notes = str(self.map.notes[key])
                lines = []
                for i in range(0, len(notes)):
                    if notes[i] == "1":
                        lines.append(i + 1)
                for _ in range(len(lines)):
                    note = Note(
                        line=lines[_],
                        display_surf=self._display_surf,
                        imageScaling=self.imageScaling,
                    )
                    note.timing = int(key) - self.timeToReact / 2
                    self.all_notes.add(note)
                self.map.notes[key] = None

    def drawRectangle(self) -> None:
        """Used to draw two rectangles as a playfield."""
        pg.draw.rect(
            self._display_surf,
            WHITE,
            pg.Rect(
                self._display_surf.get_width() / 2 - (268 * self.imageScaling),
                0,
                558 * self.imageScaling,
                self._display_surf.get_height(),
            ),
        )

        pg.draw.rect(
            self._display_surf,
            (130, 130, 130),
            pg.Rect(
                self._display_surf.get_width() / 2 - (262 * self.imageScaling),
                0,
                546 * self.imageScaling,
                self._display_surf.get_height(),
            ),
        )
        pg.draw.rect(
            self._display_surf,
            (100, 100, 100),
            pg.Rect(
                self._display_surf.get_width() / 2 - (262 * self.imageScaling),
                0,
                546 * self.imageScaling,
                4,
            ),
        )

    def updateNotes(self):
        """Used to update the position of notes relative to the audio player's timer."""
        for note in self.all_notes:
            progress = 1 - (
                (note.timing + self.waitBeforePlaying - self.audioPlayer.songPosition)
                / self.timeToReact
            )
            note.y = -(
                note.startPosition
                + ((note.startPosition - note.perfectHitPosition) * progress)
            )
            if note.y >= note.perfectHitPosition:
                # note.y = note.perfectHitPosition
                self.audioPlayer.hitSound.play()
                note.kill()

    def draw_Text(
        self, text: str, font: pg.font.Font, text_col: set, x: float, y: float
    ) -> None:
        """Used to draw a text on screen.

        Parameters
        ----------
        text : str
            Text to draw on screen.
        font : pg.font.Font
            Pygame font.
        text_col : set
            Text colour in RGB.
        x : float
            X position of the text.
        y : float
            Y position of the text.
        """
        img = font.render(text, True, text_col)
        self._display_surf.blit(img, (x, y))

    def drawNotes(self) -> None:
        """Used to draw notes on screen."""
        for note in self.all_notes:
            if note.line == 1:
                self._display_surf.blit(self.firstNote, (note._x, note.y))
            elif note.line == 2:
                self._display_surf.blit(self.secondNote, (note._x, note.y))
            elif note.line == 3:
                self._display_surf.blit(self.thirdNote, (note._x, note.y))
            elif note.line == 4:
                self._display_surf.blit(self.fourthNote, (note._x, note.y))

    def drawJudgementBar(self) -> None:
        """Used to draw a judgement bar on screen."""
        OffsetLeft = self._display_surf.get_width() / 2 - (245 * self.imageScaling)
        self._display_surf.blit(
            self.judgementBar,
            (OffsetLeft, self._display_surf.get_height() - 170 * self.imageScaling),
        )

    def drawBG(self) -> None:
        """Used to draw a background."""
        self._display_surf.fill(BLACK)
        # self.background.draw(self._display_surf)

    def drawText(self) -> None:
        """Used to draw FPS counter on screen."""
        FPS = int(self.clock.get_fps())
        if self.lowestFps > FPS and FPS != 0:
            self.lowestFps = FPS
        self.fps = str(FPS)
        fps = self.font.render(self.fps, 10, (255, 255, 255))
        self._display_surf.blit(
            fps, (self._display_surf.get_width() - fps.get_width(), 50)
        )

    def handleInput(self, eventType: pg.event.Event, key: int) -> None:
        """Used to handle keyboard input of the player.

        Parameters
        ----------
        eventType : pg.event.Event
            Pygame event.
        key : int
            Pressed keys.
        """
        if eventType == KEYDOWN:
            self.audioPlayer.hitSound.play()
            if key == K_a:
                self.pressedKeys[0] = True
            if key == K_s:
                self.pressedKeys[1] = True
            if key == K_k:
                self.pressedKeys[2] = True
            if key == K_l:
                self.pressedKeys[3] = True
        elif eventType == KEYUP:
            if key == K_a:
                self.pressedKeys[0] = False
            if key == K_s:
                self.pressedKeys[1] = False
            if key == K_k:
                self.pressedKeys[2] = False
            if key == K_l:
                self.pressedKeys[3] = False

    def resizeSprites(self) -> None:
        """Used to resize all sprites."""
        currentSize = self._display_surf.get_size()
        self.imageScaling = currentSize[1] / 720
        # self.BgSprite = pg.transform.smoothscale(
        #     self._BgSprite, self._display_surf.get_size()
        # )
        self.JudgementCircleSprite = pg.transform.smoothscale_by(
            self._JudgementCircleSprite, factor=self.imageScaling
        )
        for note in self.all_notes:
            note.updateimageScaling(self.imageScaling)

    def waitBeforePlayingSong(self) -> None:
        """Used to wait before playing a song."""
        if (
            pg.time.get_ticks() >= self.waitBeforePlaying
            and not self.startedPlayingSong
        ):
            self.audioPlayer.playSong()
            self.startedPlayingSong = True

    def on_event(self, event) -> None:
        """Used to handle pygame events.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        if event.type == QUIT:
            self._running = False
        if event.type == KEYDOWN:
            if self.gamePaused:
                if event.key == K_RETURN and self.selected_option == 0:
                    self.audioPlayer.mixer.music.unpause()
                    self.gamePaused = False
                if event.key == K_RETURN and self.selected_option == 1:
                    pass
                if event.key == K_RETURN and self.selected_option == 2:
                    self._running = False
                if event.key == K_ESCAPE:
                    self.audioPlayer.mixer.music.unpause()
                    self.gamePaused = False
                if event.key == K_DOWN:
                    if self.selected_option < 2:
                        self.selected_option += 1
                    else:
                        self.selected_option = 0
                if event.key == K_UP:
                    if self.selected_option > 0:
                        self.selected_option -= 1
                    else:
                        self.selected_option = 2
            else:
                if event.key == K_ESCAPE:
                    self.audioPlayer.mixer.music.pause()
                    self.gamePaused = True
        if event.type == KEYDOWN or event.type == KEYUP:
            self.handleInput(eventType=event.type, key=event.key)
        if event.type == WINDOWRESIZED:
            self.resizeSprites()

    def on_loop(self) -> None:
        """Used to perform a game loop."""
        if not self.gamePaused:
            self.waitBeforePlayingSong()
        self.spawnNotes()
        if self.gamePaused == False:
            self.updateNotes()
            self.audioPlayer.update()

    def drawTextWithShadow(
        self,
        text: str,
        font: pg.font.Font,
        text_col: set,
        shadow_col: set,
        x: float,
        y: float,
        shadow_offset: float,
    ) -> None:
        """Used to draw a text with shadow on screen.

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
        x : float
            X position of the text.
        y : float
            Y position of the text.
        shadow_offset : float
            Offset of the shadow.
        """
        img = font.render(text, True, shadow_col)
        self._display_surf.blit(img, (x + shadow_offset, y + shadow_offset))
        img = font.render(text, True, text_col)
        self._display_surf.blit(img, (x, y))

    def on_render(self) -> None:
        """Used to perform rendering on screen."""
        self.clock.tick(FPS)
        self._display_surf.fill(BLACK)
        self.other_sprites.draw(self._display_surf)
        self.drawRectangle()
        self.drawJudgementBar()
        self.drawNotes()
        self.drawText()
        if self.gamePaused:
            s = pg.Surface(self.size, pg.SRCALPHA)  # per-pixel alpha
            s.fill((0, 0, 0, 128))  # notice the alpha value in the color
            self._display_surf.blit(s, (0, 0))
            self.drawTextWithShadow(
                "Game paused",
                self.font,
                WHITE,
                BLACK,
                self._display_surf.get_width() / 2 - 150,
                100,
                4,
            )
            if self.selected_option == 0:
                resume_text = f"> {self.menu_text[0]}"
            else:
                resume_text = self.menu_text[0]
            if self.selected_option == 1:
                retry_text = f"> {self.menu_text[1]}"
            else:
                retry_text = self.menu_text[1]

            if self.selected_option == 2:
                quit_text = f"> {self.menu_text[2]}"
            else:
                quit_text = self.menu_text[2]

            self.drawTextWithShadow(
                resume_text,
                self.font,
                WHITE,
                BLACK,
                self._display_surf.get_width() / 2 - 150,
                220,
                4,
            )
            self.drawTextWithShadow(
                retry_text,
                self.font,
                WHITE,
                BLACK,
                self._display_surf.get_width() / 2 - 150,
                300,
                4,
            )
            self.drawTextWithShadow(
                quit_text,
                self.font,
                WHITE,
                BLACK,
                self._display_surf.get_width() / 2 - 150,
                380,
                4,
            )
        pg.display.update()

    def on_cleanup(self) -> None:
        """Used to handle cleanup when the game is closed."""
        print(self.lowestFps)
        pg.quit()

    def on_execute(self) -> None:
        """Used to perform a game logic."""
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    # flags = FULLSCREEN
    flags = RESIZABLE
    game = Game(width=1280, height=720, initializationFlags=flags)
    game.on_execute()
