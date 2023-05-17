import json
import time
import pygame as pg
import os
from pygame.locals import *


# imports
import spritesheet
import audioplayer
import converter
import text

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
        self,
        line: int,
        image: pg.surface.Surface,
        timing: int,
        display_surf: pg.surface.Surface,
        imageScaling: float,
    ) -> None:
        """
        Parameters
        ----------
        line : int
            Line number to which the note belongs.
        image : pg.surface.Surface
            Image representing a note.
        timing : int
            Timing of the note.
        display_surf : pg.surface.Surface
            Display surface.
        imageScaling : float
            Scaling of the note sprite.
        """
        pg.sprite.Sprite.__init__(self)
        self._display_surf = display_surf
        self.image = image
        self.imageScaling = imageScaling
        self.startPosition = 0
        self.perfectHitPosition = (
            self._display_surf.get_height() - 170 * self.imageScaling
        )
        self.timing = timing
        self.line = line
        self.OffsetLeft = self._display_surf.get_width() / 2 - 258
        self.MarginBetweenNotes = 132 * self.imageScaling
        self.isClickable = False
        self._x = self.OffsetLeft + (self.line - 1) * self.MarginBetweenNotes
        self.y = -140

    def updateimageScaling(self, imageScaling: float):
        """Used to update image scaling."""
        self.imageScaling = imageScaling

    def draw(self, surface: pg.surface.Surface):
        surface.blit(self.image, (self._x, self.y))


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
        self.map = Map("src/maps/AiAe/")
        self.audioPlayer = audioplayer.AudioPlayer(self.map.bpm, self.map.audio)

        self.menu_text = ["Resume", "Retry", "Quit"]
        self.selected_option = 0
        self.score = 0
        self.combo = 0
        self.accuracy = 100.0
        self.lastGrade = ""
        self.gamePaused = False
        self.backgroundAlpha = 160
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
                    if lines[_] == 1:
                        image = self.firstNote
                    elif lines[_] == 2:
                        image = self.secondNote
                    elif lines[_] == 3:
                        image = self.thirdNote
                    elif lines[_] == 4:
                        image = self.fourthNote
                    timing = int(key) - self.timeToReact / 2
                    note = Note(
                        line=lines[_],
                        image=image,
                        timing=timing,
                        display_surf=self._display_surf,
                        imageScaling=self.imageScaling,
                    )
                    self.all_notes.add(note)
                self.map.notes[key] = None

    def drawRectangle(self) -> None:
        """Used to draw two rectangles as a playfield."""
        black_surf = pg.Surface((546, self._display_surf.get_height()))
        black_surf.fill((130, 130, 130))
        white_surf = pg.Surface((558, self._display_surf.get_height()))
        white_surf.fill(WHITE)
        self._display_surf.blit(
            white_surf,
            (self._display_surf.get_width() / 2 - white_surf.get_width() / 2, 0),
        )
        self._display_surf.blit(
            black_surf,
            (self._display_surf.get_width() / 2 - black_surf.get_width() / 2, 0),
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
            if progress > 0.7:
                note.isClickable = True
            # print(self.audioPlayer.songPosition - note.timing)
            if progress > 1.3:
                #     self.audioPlayer.hitSound.play()
                self.combo = 0
                note.kill()

    def drawNotes(self) -> None:
        """Used to draw notes on screen."""
        for note in self.all_notes:
            note.draw(self._display_surf)

    def drawJudgementBar(self) -> None:
        """Used to draw a judgement bar on screen."""
        OffsetLeft = (
            self._display_surf.get_width() / 2 - self.judgementBar.get_width() / 2
        )
        self._display_surf.blit(
            self.judgementBar,
            (OffsetLeft, self._display_surf.get_height() - 170 * self.imageScaling),
        )

    def drawBG(self) -> None:
        """Used to draw a background."""
        self._display_surf.fill(BLACK)
        # self.background.draw(self._display_surf)

    def drawFPS(self) -> None:
        """Used to draw FPS counter on screen."""
        FPS = int(self.clock.get_fps())
        if self.lowestFps > FPS and FPS != 0:
            self.lowestFps = FPS
        self.fps = f"fps: {FPS}"
        fps = text.TextWithShadow(
            self.fps, font=self.font, text_col=WHITE, shadow_col=BLACK, shadow_offset=4
        )
        fps.draw(
            self._display_surf.get_width() - fps.get_width(),
            self._display_surf.get_height() - fps.get_height(),
            self._display_surf,
        )

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

    def get_grade(self, progress: float) -> str:
        if progress >= 0.75 and progress < 0.8 or progress > 1.2 and progress <= 1.25:
            return "Good!"
        elif progress >= 0.8 and progress < 0.95 or progress > 1.05 and progress <= 1.2:
            return "Great!"
        elif progress >= 0.95 and progress <= 1.05:
            return "Perfect!"
        else:
            return "Miss!"

    def add_score(self, progress: float) -> None:
        if self.combo < 10:
            score_multiplier = 1
        else:
            score_multiplier = int(self.combo * 0.1)
        if progress >= 0.75 and progress < 0.8 or progress > 1.2 and progress <= 1.25:
            self.score += 50 * score_multiplier
        elif progress >= 0.8 and progress < 0.9 or progress > 1.1 and progress <= 1.2:
            self.score += 100 * score_multiplier
        elif progress >= 0.95 and progress <= 1.05:
            self.score += 300 * score_multiplier

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
        if event.type == KEYDOWN:
            if event.key == K_d and not self.pressedKeys[0]:
                self.pressedKeys[0] = True
                for note in self.all_notes:
                    if note.line == 1 and note.isClickable:
                        progress = 1 - (
                            (
                                note.timing
                                + self.waitBeforePlaying
                                - self.audioPlayer.songPosition
                            )
                            / self.timeToReact
                        )
                        self.add_score(progress=progress)
                        self.lastGrade = self.get_grade(progress=progress)
                        if self.lastGrade != "Miss!":
                            self.combo += 1
                        else:
                            self.combo == 0
                        self.audioPlayer.hitSound.play()
                        note.kill()
                        break
            if event.key == K_f and not self.pressedKeys[1]:
                self.pressedKeys[1] = True
                for note in self.all_notes:
                    if note.line == 2 and note.isClickable:
                        progress = 1 - (
                            (
                                note.timing
                                + self.waitBeforePlaying
                                - self.audioPlayer.songPosition
                            )
                            / self.timeToReact
                        )
                        self.add_score(progress=progress)
                        self.lastGrade = self.get_grade(progress=progress)
                        if self.lastGrade != "Miss!":
                            self.combo += 1
                        else:
                            self.combo == 0
                        self.audioPlayer.hitSound.play()
                        note.kill()
                        break
            if event.key == K_j and not self.pressedKeys[2]:
                self.pressedKeys[2] = True
                for note in self.all_notes:
                    if note.line == 3 and note.isClickable:
                        progress = 1 - (
                            (
                                note.timing
                                + self.waitBeforePlaying
                                - self.audioPlayer.songPosition
                            )
                            / self.timeToReact
                        )
                        self.add_score(progress=progress)
                        self.lastGrade = self.get_grade(progress=progress)
                        if self.lastGrade != "Miss!":
                            self.combo += 1
                        else:
                            self.combo == 0
                        self.audioPlayer.hitSound.play()
                        note.kill()
                        break
            if event.key == K_k and not self.pressedKeys[3]:
                self.pressedKeys[3] = True
                for note in self.all_notes:
                    if note.line == 4 and note.isClickable:
                        progress = 1 - (
                            (
                                note.timing
                                + self.waitBeforePlaying
                                - self.audioPlayer.songPosition
                            )
                            / self.timeToReact
                        )
                        self.add_score(progress=progress)
                        self.lastGrade = self.get_grade(progress=progress)
                        if self.lastGrade != "Miss!":
                            self.combo += 1
                        else:
                            self.combo == 0
                        self.audioPlayer.hitSound.play()
                        note.kill()
                        break

        if event.type == KEYUP:
            if event.key == K_d and self.pressedKeys[0]:
                self.pressedKeys[0] = False
            if event.key == K_f and self.pressedKeys[1]:
                self.pressedKeys[1] = False
            if event.key == K_j and self.pressedKeys[2]:
                self.pressedKeys[2] = False
            if event.key == K_k and self.pressedKeys[3]:
                self.pressedKeys[3] = False
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

    def on_render(self) -> None:
        """Used to perform rendering on screen."""
        self.clock.tick(FPS)
        self._display_surf.fill(BLACK)
        self.other_sprites.draw(self._display_surf)
        s = pg.Surface(self.size, pg.SRCALPHA)  # per-pixel alpha
        s.fill((0, 0, 0, self.backgroundAlpha))  # notice the alpha value in the color
        self._display_surf.blit(s, (0, 0))
        self.drawRectangle()
        self.drawJudgementBar()
        self.drawNotes()
        self.drawFPS()
        score = text.TextWithShadow(
            str(self.score),
            self.font,
            WHITE,
            BLACK,
            4,
        )
        score.draw(
            self._display_surf.get_width() - score.get_width(), 0, self._display_surf
        )
        lastGrade = text.TextWithShadow(
            self.lastGrade,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        lastGrade.draw(
            self._display_surf.get_width() / 2 - lastGrade.get_width() / 2,
            300,
            self._display_surf,
        )
        combo = text.TextWithShadow(
            str(self.combo),
            self.font,
            WHITE,
            BLACK,
            4,
        )
        combo.draw(
            self._display_surf.get_width() / 2 - combo.get_width() / 2,
            200,
            self._display_surf,
        )
        if self.gamePaused:
            s = pg.Surface(self.size, pg.SRCALPHA)  # per-pixel alpha
            s.fill((0, 0, 0, 128))  # notice the alpha value in the color
            self._display_surf.blit(s, (0, 0))
            paused_surf = text.TextWithShadow(
                "Game paused",
                self.font,
                WHITE,
                BLACK,
                4,
            )
            paused_surf.draw(
                self._display_surf.get_width() / 2 - paused_surf.get_width() / 2,
                100,
                self._display_surf,
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

            resume_surf = text.TextWithShadow(
                resume_text,
                self.font,
                WHITE,
                BLACK,
                4,
            )
            resume_surf.draw(
                self._display_surf.get_width() / 2 - 150, 220, self._display_surf
            )
            retry_surf = text.TextWithShadow(
                retry_text,
                self.font,
                WHITE,
                BLACK,
                4,
            )
            retry_surf.draw(
                self._display_surf.get_width() / 2 - 150, 300, self._display_surf
            )
            quit_surf = text.TextWithShadow(
                quit_text,
                self.font,
                WHITE,
                BLACK,
                4,
            )
            quit_surf.draw(
                self._display_surf.get_width() / 2 - 150, 380, self._display_surf
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
