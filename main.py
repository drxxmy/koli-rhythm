import json
import random
import pygame as pg
import os
from enum import Enum
from pygame.locals import *


# imports
import spritesheet
import audioplayer
import text
import chart

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Constants
FPS = 1000


class GameState(Enum):
    in_game = 0
    main_menu = 1
    settings_menu = 2
    paused = 3
    chart_select_menu = 4
    difficulty_select_menu = 5


class Settings:
    def __init__(self) -> None:
        self.note_speed = 1.0
        self.background_dim = 100
        self.volume = 100
        self.time_to_react = 400

    def increment_note_speed(self):
        if self.time_to_react > 200:
            self.note_speed += 0.1
            self.time_to_react -= 25

    def decrement_note_speed(self):
        if self.time_to_react < 600:
            self.note_speed -= 0.1
            self.time_to_react += 25


class HitGlow:
    def __init__(self, line: int, display_surf: pg.surface.Surface) -> None:
        self.surf = pg.Surface((120, 120), SRCALPHA)
        self.alphaLevel = 0
        self.time = pg.time.get_ticks()
        self.timer = 300  # ms
        self.color = [255, 255, 255, self.alphaLevel]
        self.line = line
        self.offset_left = display_surf.get_width() / 2 - 258
        self.notes_margin = 132
        self._x = self.offset_left + (self.line - 1) * self.notes_margin
        self.y = display_surf.get_height() - 170
        self.particles = []

    def emit(self, surface):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][1] += particle[2][0]
                particle[0][0] += particle[2][1]
                particle[1] -= 0.2
                pg.draw.circle(
                    surface, (255, 255, 255, 1), particle[0], int(particle[1])
                )

    def add_particles(self):
        pos_x = self._x + 60
        pos_y = self.y + 60
        radius = 15
        direction_x = random.randint(-2, 2)
        direction_y = random.randint(-2, 2)
        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y]]
        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy

    def draw(self, surface: pg.surface.Surface) -> None:
        surface.blit(self.surf, (self._x, self.y))

    def update(self) -> None:
        now = pg.time.get_ticks()
        if now > self.time + self.timer:
            return True
        else:
            return False


class Hit:
    def __init__(self, progress: float) -> None:
        self.surf = pg.Surface((5, 18), SRCALPHA)
        self.progress = progress
        self.alphaLevel = 255
        self.time = pg.time.get_ticks()
        self.delay = 30  # ms
        self.perfect_color = [104, 158, 227, self.alphaLevel]
        self.great_color = [124, 208, 139, self.alphaLevel]
        self.good_color = [227, 158, 104, self.alphaLevel]
        self.miss_color = [227, 111, 105, self.alphaLevel]
        self.color = self.get_correct_color()

    def get_correct_color(self) -> list:
        if (
            self.progress >= 0.75
            and self.progress < 0.8
            or self.progress > 1.2
            and self.progress <= 1.25
        ):
            return self.good_color
        elif (
            self.progress >= 0.8
            and self.progress < 0.95
            or self.progress > 1.05
            and self.progress <= 1.2
        ):
            return self.great_color
        elif self.progress >= 0.95 and self.progress <= 1.05:
            return self.perfect_color
        else:
            return self.miss_color

    def get_offset(self) -> float:
        coef = ((self.progress - 1) * 3.33) * 98
        return coef

    def ready_to_delete(self) -> bool:
        if self.color[3] == 0:
            return True
        else:
            return False

    def draw(self, surface: pg.surface.Surface) -> None:
        self.surf.fill(self.color)
        surface.blit(
            self.surf,
            (  # + 98 - 98 края
                surface.get_width() / 2 - self.surf.get_width() / 2 + self.get_offset(),
                393,
            ),
        )

    def update(self) -> None:
        now = pg.time.get_ticks()
        if now > self.time + self.delay:
            if self.color[3] > 0:
                self.color[3] -= 17
            self.time = now


class UserInterface:
    def __init__(self, score: int, last_grade: str, combo: int, fps: int):
        self.font = pg.font.Font(os.path.join("fonts", "PixeloidSansBold.ttf"), 45)
        self.score = text.TextWithShadow(
            f"{score:,d}",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        self.lastGrade = text.TextWithShadow(
            last_grade,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        self.combo = text.TextWithShadow(
            str(combo),
            self.font,
            WHITE,
            BLACK,
            4,
        )
        self.fps = text.TextWithShadow(str(int(fps)), self.font, WHITE, BLACK, 4)

    def update_text(self, score: int, last_grade: str, combo: int, fps: int):
        self.score = text.TextWithShadow(
            f"{score:,d}",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        self.lastGrade = text.TextWithShadow(
            last_grade,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        self.combo = text.TextWithShadow(
            str(combo),
            self.font,
            WHITE,
            BLACK,
            4,
        )
        self.fps = text.TextWithShadow(str(int(fps)), self.font, WHITE, BLACK, 4)

    def draw(self, surface: pg.Surface):
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
        self.fps.draw(
            surface.get_width() - self.fps.get_width(),
            surface.get_height() - self.fps.get_height(),
            surface,
        )


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
    """Class representing a game note."""

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
            Line number to which the note belongs.
        image : pg.surface.Surface
            Image representing a note.
        timing : int
            Timing of the note.
        display_surf : pg.surface.Surface
            Display surface.
        """
        pg.sprite.Sprite.__init__(self)
        self.screen = display_surf
        self.image = image
        self.startPosition = 0
        self.perfectHitPosition = self.screen.get_height() - 170
        self.timing = timing
        self.line = line
        self.offset_left = self.screen.get_width() / 2 - 258
        self.notes_margin = 132
        self.isClickable = False
        self.rect = self.image.get_rect()
        self.rect.x = self.offset_left + (self.line - 1) * self.notes_margin
        self.rect.y = -140

    def update_y_pos(self, progress) -> None:
        self.rect.y = -(
            self.startPosition
            + ((self.startPosition - self.perfectHitPosition) * progress)
        )


class SingleNote(Note):
    def __init__(self, y: int, line: int) -> None:
        super().__init__(y, line)


class LongNote(Note):
    def __init__(self, x: int, y: int, line: int, length: int) -> None:
        super().__init__(x, y, line)
        self.length = length


class Game:
    """The main class that implements the logic of the game.

    Methods
    -------
    on_init()
        Used to initialize the pygame module, game window and some variables.
    load_resources()
        Used to load resources of the game. (Fonts, sprites etc)
    spawn_notes()
        Used to spawn notes of certain chart.
    draw_rectangle()
        Used to draw two rectangles as a playfield.
    update_notes()
        Used to update the position of notes relative to the audio player's timer.
    drawText(text, font, text_col, x, y)
        Used to draw a text on screen.
    draw_notes()
        Used to draw notes on screen.
    draw_bar()
        Used to draw a judgement bar on screen.
    draw_bg()
        Used to draw a background.
    handleInput(eventType, key)
        Used to handle keyboard input of the player.
    resizeSprites()
        Used to resize all sprites.
    wait_before_playing_song()
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
        self.settings = Settings()
        self._flags = initializationFlags
        self.size = self.width, self.height = width, height

    def on_init(self) -> None:
        """Used to initialize the pygame module, game window and some variables."""
        pg.init()
        pg.display.set_caption("Koli Rhythm")
        self.clock = pg.time.Clock()
        self.lowestFps = 99999
        self.screen = pg.display.set_mode(self.size, self._flags)

        self.enter_is_pressed = False
        self.pressed_keys = [False, False, False, False]
        self.selected_chart = None  # chart.Chart(chart_name="Freedom Dive")
        self.selected_difficulty = None  # self.selected_chart.difficulties[0]

        self.audioPlayer = None

        self.main_menu_text = ["Play", "Settings", "Quit"]
        self.main_menu_selected = 0

        self.charts = self.get_charts()
        self.chart_select_menu_selected = 0

        self.difficulties = None
        self.difficulties_select_menu_selected = 0

        self.pause_menu_text = ["Resume", "Retry", "Leave"]
        self.pause_menu_selected = 0

        self.settings_menu_text = [
            "Note Speed: ",
            "Background Dim: ",
            "Volume: ",
            "Back",
        ]
        self.settings_menu_selected = 0

        self.game_state = GameState.main_menu

        self.time_since_game_start = pg.time.get_ticks()
        self.starting_chart_time = 0
        self.fps = self.clock.get_fps()
        self.score = 0
        self.combo = 0
        self.accuracy = 100.0
        self.lastGrade = ""
        self.spawned_notes_timings = []
        self.user_interface = UserInterface(
            score=self.score, last_grade=self.lastGrade, combo=self.combo, fps=self.fps
        )

        self.backgroundAlpha = 160
        self.waitBeforePlaying = 1000
        self.startedPlayingSong = False

        self.all_notes = pg.sprite.Group()
        self.all_recent_hits = []
        self.all_hit_glows = []
        self.other_sprites = pg.sprite.RenderUpdates()
        self.load_resources()

    def get_charts(self) -> list:
        charts = [
            f.name for f in os.scandir(os.path.join("src", "charts")) if f.is_dir()
        ]
        return charts

    def load_resources(self) -> None:
        """Used to load resources of the game. (Fonts, sprites etc)"""
        self.notesSheet = spritesheet.SpriteSheet(
            os.path.join("sprites", "notes", "notesSheet.png")
        )
        self.firstNote = self.notesSheet.get_image(0, 120, 120, 1, BLACK)
        self.secondNote = self.notesSheet.get_image(1, 120, 120, 1, BLACK)
        self.thirdNote = self.notesSheet.get_image(2, 120, 120, 1, BLACK)
        self.fourthNote = self.notesSheet.get_image(3, 120, 120, 1, BLACK)
        self.bar = pg.image.load(os.path.join("sprites", "notes", "barSheet.png"))
        self.font = pg.font.Font(os.path.join("fonts", "PixeloidSansBold.ttf"), 45)

    def update_hits(self) -> None:
        for hit in self.all_recent_hits:
            hit.update()
            if hit.ready_to_delete():
                self.all_recent_hits.remove(hit)

    def update_hit_glows(self) -> None:
        for hit_glow in self.all_hit_glows:
            if hit_glow.update():
                self.all_hit_glows.remove(hit_glow)

    def get_spawn_lines(self, note_positions: str) -> list:
        spawn_lines = []
        for i in range(0, len(note_positions)):
            if note_positions[i] == "1":
                spawn_lines.append(i + 1)
        return spawn_lines

    def get_image_for_note(self, line: int):
        if line == 1:
            return self.firstNote
        elif line == 2:
            return self.secondNote
        elif line == 3:
            return self.thirdNote
        elif line == 4:
            return self.fourthNote

    def spawn_notes(self) -> None:
        """Used to spawn notes of certain chart.

        It checks if the audio player timer is equal or more than note timings
        and creates a new instance of the note corresponding to the desired line
        above the screen.
        """
        for key in self.selected_difficulty.notes:
            if (
                self.audioPlayer.songPosition >= int(key)
                and key not in self.spawned_notes_timings
            ):
                note_positions = str(self.selected_difficulty.notes[key])
                spawn_lines = self.get_spawn_lines(note_positions=note_positions)
                timing = int(key) - self.settings.time_to_react / 2
                for line in spawn_lines:
                    image = self.get_image_for_note(line)
                    note = Note(
                        line=line,
                        image=image,
                        timing=timing,
                        display_surf=self.screen,
                    )
                    self.all_notes.add(note)
                self.spawned_notes_timings.append(key)

    def draw_rectangle(self) -> None:
        """Used to draw two rectangles as a playfield."""
        black_surf = pg.Surface((546, self.screen.get_height()))
        black_surf.fill((100, 100, 100))
        white_surf = pg.Surface((558, self.screen.get_height()))
        white_surf.fill(WHITE)
        self.screen.blit(
            white_surf,
            (self.screen.get_width() / 2 - white_surf.get_width() / 2, 0),
        )
        self.screen.blit(
            black_surf,
            (self.screen.get_width() / 2 - black_surf.get_width() / 2, 0),
        )

    def update_notes(self):
        """Used to update the position of notes relative to the audio player's timer."""
        for note in self.all_notes:
            progress = self.get_note_progress(note)
            note.update_y_pos(progress)
            if progress >= 0.7:
                note.isClickable = True
            if progress > 1.3:
                self.combo = 0
                note.kill()

    def get_note_progress(self, note: Note):
        progress = 1 - (
            (note.timing + self.waitBeforePlaying - self.audioPlayer.songPosition)
            / self.settings.time_to_react
        )
        return progress

    def destroy_note(
        self,
        line: int,
    ) -> None:
        for note in self.all_notes:
            if note.line == line and note.isClickable:
                self.audioPlayer.hitSound.play()
                note.kill()
                break

    def draw_notes(self) -> None:
        """Used to draw notes on screen."""
        self.all_notes.draw(self.screen)

    def draw_bar(self) -> None:
        """Used to draw a judgement bar on screen."""
        offset_left = self.screen.get_width() / 2 - self.bar.get_width() / 2
        self.screen.blit(
            self.bar,
            (offset_left, self.screen.get_height() - 170),
        )

    def draw_bg(self) -> None:
        """Used to draw a background."""
        self.screen.fill(BLACK)
        # self.background.draw(self.screen)

    def get_fps(self) -> int:
        fps = int(self.clock.get_fps())
        return fps

    def wait_before_playing_song(self) -> None:
        """Used to wait before playing a song."""

        if not self.startedPlayingSong:
            self.elapsed_time = pg.time.get_ticks() - self.starting_chart_time
        if self.elapsed_time >= self.waitBeforePlaying and not self.startedPlayingSong:
            self.audioPlayer.playSong()
            self.startedPlayingSong = True

    def draw_hitbar(self) -> None:
        hitbar_surf = pg.Surface((200, 5))
        hitbar_surf.fill((160, 160, 160))
        self.screen.blit(
            hitbar_surf,
            (self.screen.get_width() / 2 - hitbar_surf.get_width() / 2, 400),
        )
        hitbar_center_surf = pg.Surface((5, 20))
        hitbar_center_surf.fill((180, 180, 180))
        self.screen.blit(
            hitbar_center_surf,
            (
                self.screen.get_width() / 2 - hitbar_center_surf.get_width() / 2,
                392,
            ),
        )

    def draw_hit(self) -> None:
        hitbar_center_surf = pg.Surface((5, 18))
        hitbar_center_surf.fill((171, 186, 186))
        self.screen.blit(
            hitbar_center_surf,
            (
                self.screen.get_width() / 2 - hitbar_center_surf.get_width() + 10,
                393,
            ),
        )

    def calculate_accuracy(self):
        # TODO - Find Formula
        pass

    def change_combo(self, grade: str) -> None:
        if grade != "Miss!":
            self.combo += 1
        else:
            self.combo = 0

    def get_grade(self, progress: float) -> str:
        if progress >= 0.75 and progress < 0.8 or progress > 1.2 and progress <= 1.25:
            return "Good!"
        elif progress >= 0.8 and progress < 0.95 or progress > 1.05 and progress <= 1.2:
            return "Great!"
        elif progress >= 0.95 and progress <= 1.05:
            return "Perfect!"
        else:
            return "Miss!"

    def add_score(self, grade: str) -> None:
        if self.combo < 10:
            score_multiplier = 1
        else:
            score_multiplier = int(self.combo * 0.1)
        if grade == "Good!":
            self.score += 50 * score_multiplier
        elif grade == "Great!":
            self.score += 100 * score_multiplier
        elif grade == "Perfect!":
            self.score += 300 * score_multiplier

    def retry(self) -> None:
        self.all_notes.empty()
        self.starting_chart_time = pg.time.get_ticks()
        self.startedPlayingSong = False
        self.spawned_notes_timings.clear()
        self.score = 0
        self.combo = 0
        self.accuracy = 100.0
        self.audioPlayer.reset_song_position()
        self.audioPlayer.playSong()
        print(f"{self.audioPlayer.songPosition} 0 0")

    def handle_note(self, line: int) -> None:
        self.pressed_keys[line - 1] = True
        for note in self.all_notes:
            self.destroy_note(line)
            progress = self.get_note_progress(note)
            self.lastGrade = self.get_grade(progress=progress)
            hit = Hit(progress=progress)
            # hit_glow = HitGlow(note.line, self.screen)
            # for _ in range(10):
            #     hit_glow.add_particles()
            # self.all_hit_glows.append(hit_glow)
            self.all_recent_hits.append(hit)
            self.add_score(self.lastGrade)
            self.change_combo(self.lastGrade)
            self.audioPlayer.hitSound.play()
            break

    def handle_main_menu(self, event) -> None:
        if event.type == KEYDOWN:
            if not self.enter_is_pressed:
                if event.key == K_RETURN and self.main_menu_selected == 0:
                    self.game_state = GameState.chart_select_menu
                    self.charts = self.get_charts()
                    self.main_menu_selected = 0
                if event.key == K_RETURN and self.main_menu_selected == 1:
                    self.game_state = GameState.settings_menu
                    self.main_menu_selected = 0
                if event.key == K_RETURN and self.main_menu_selected == 2:
                    self._running = False
                self.enter_is_pressed = True
            if event.key == K_ESCAPE:
                self._running = False
            if event.key == K_DOWN:
                if self.main_menu_selected < 2:
                    self.main_menu_selected += 1
                else:
                    self.main_menu_selected = 0
            if event.key == K_UP:
                if self.main_menu_selected > 0:
                    self.main_menu_selected -= 1
                else:
                    self.main_menu_selected = 2
        if event.type == KEYUP:
            self.enter_is_pressed = False

    def handle_chart_select_menu(self, event) -> None:
        if event.type == KEYDOWN:
            if not self.enter_is_pressed:
                if event.key == K_RETURN:
                    self.selected_chart = chart.Chart(
                        self.charts[self.chart_select_menu_selected]
                    )
                    self.difficulties = self.selected_chart.get_all_difficulties()
                    self.background = Background(self.selected_chart.background)
                    self.other_sprites.add(self.background)
                    self.game_state = GameState.difficulty_select_menu
                    self.enter_is_pressed = True
            if event.key == K_ESCAPE:
                self.game_state = GameState.main_menu
            if event.key == K_DOWN:
                if self.chart_select_menu_selected < len(self.charts) - 1:
                    self.chart_select_menu_selected += 1
                else:
                    self.chart_select_menu_selected = 0
            if event.key == K_UP:
                if self.chart_select_menu_selected > 0:
                    self.chart_select_menu_selected -= 1
                else:
                    self.chart_select_menu_selected = len(self.charts) - 1

        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

    def handle_difficulty_select_menu(self, event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.game_state = GameState.chart_select_menu
                self.chart = None
            if not self.enter_is_pressed:
                if event.key == K_RETURN:
                    self.selected_difficulty = self.difficulties[
                        self.difficulties_select_menu_selected
                    ]
                    self.game_state = GameState.in_game
                    self.audioPlayer = audioplayer.AudioPlayer(
                        self.selected_chart.bpm, self.selected_chart.audio
                    )
                    self.background = Background(self.selected_chart.background)
                    self.enter_is_pressed = True
            if event.key == K_DOWN:
                if self.difficulties_select_menu_selected < len(self.difficulties) - 1:
                    self.difficulties_select_menu_selected += 1
                else:
                    self.difficulties_select_menu_selected = 0
                print(self.difficulties_select_menu_selected)
            if event.key == K_UP:
                if self.difficulties_select_menu_selected > 0:
                    self.difficulties_select_menu_selected -= 1
                else:
                    self.difficulties_select_menu_selected = len(self.difficulties) - 1
                print(self.difficulties_select_menu_selected)
        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

    def handle_settings_menu(self, event) -> None:
        if event.type == KEYDOWN:
            # if event.key == K_RETURN and self.settings_menu_selected == 0:
            #     pass
            # if event.key == K_RETURN and self.settings_menu_selected == 1:
            #     pass
            # if event.key == K_RETURN and self.settings_menu_selected == 2:
            #     pass
            if event.key == K_RETURN and self.settings_menu_selected == 3:
                self.game_state = GameState.main_menu
                self.settings_menu_selected = 0
            if event.key == K_ESCAPE:
                pass
            if event.key == K_LEFT and self.settings_menu_selected == 0:
                if self.settings.note_speed > 0.6:
                    self.settings.note_speed -= 0.1
            if event.key == K_RIGHT and self.settings_menu_selected == 0:
                if self.settings.note_speed < 2:
                    self.settings.note_speed += 0.1

            if event.key == K_LEFT and self.settings_menu_selected == 1:
                if self.settings.background_dim > 0:
                    self.settings.background_dim -= 5
            if event.key == K_RIGHT and self.settings_menu_selected == 1:
                if self.settings.background_dim < 100:
                    self.settings.background_dim += 5

            if event.key == K_LEFT and self.settings_menu_selected == 2:
                if self.settings.volume > 0:
                    self.settings.volume -= 5
            if event.key == K_RIGHT and self.settings_menu_selected == 2:
                if self.settings.volume < 100:
                    self.settings.volume += 5

            if event.key == K_DOWN:
                if self.settings_menu_selected < 3:
                    self.settings_menu_selected += 1
                else:
                    self.settings_menu_selected = 0
            if event.key == K_UP:
                if self.settings_menu_selected > 0:
                    self.settings_menu_selected -= 1
                else:
                    self.settings_menu_selected = 3

    def handle_pause_menu(self, event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_RETURN and self.pause_menu_selected == 0:
                self.audioPlayer.mixer.music.unpause()
                self.game_state = GameState.in_game
                self.pause_menu_selected = 0
            if event.key == K_RETURN and self.pause_menu_selected == 1:
                self.retry()
                self.game_state = GameState.in_game
                self.pause_menu_selected = 0
            if event.key == K_RETURN and self.pause_menu_selected == 2:
                self.game_state = GameState.main_menu
                self.pause_menu_selected = 0
            if event.key == K_ESCAPE:
                self.audioPlayer.mixer.music.unpause()
                self.game_state = GameState.in_game
                self.pause_menu_selected = 0
            if event.key == K_DOWN:
                if self.pause_menu_selected < 2:
                    self.pause_menu_selected += 1
                else:
                    self.pause_menu_selected = 0
            if event.key == K_UP:
                if self.pause_menu_selected > 0:
                    self.pause_menu_selected -= 1
                else:
                    self.pause_menu_selected = 2

    def draw_main_menu(self) -> None:
        self.screen.fill(BLACK)
        # -- Update text of the buttons -- #
        if self.main_menu_selected == 0:
            play_text = f"> {self.main_menu_text[0]} <"
        else:
            play_text = self.main_menu_text[0]

        if self.main_menu_selected == 1:
            settings_text = f"> {self.main_menu_text[1]} <"
        else:
            settings_text = self.main_menu_text[1]

        if self.main_menu_selected == 2:
            quit_text = f"> {self.main_menu_text[2]} <"
        else:
            quit_text = self.main_menu_text[2]

        title_surf = text.TextWithShadow(
            "Koli Rhythm",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        title_surf.draw(
            self.screen.get_width() / 2 - title_surf.get_width() / 2,
            100,
            self.screen,
        )

        play_surf = text.TextWithShadow(
            play_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        play_surf.draw(
            self.screen.get_width() / 2 - play_surf.get_width() / 2,
            220,
            self.screen,
        )
        settings_surf = text.TextWithShadow(
            settings_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        settings_surf.draw(
            self.screen.get_width() / 2 - settings_surf.get_width() / 2,
            300,
            self.screen,
        )
        quit_surf = text.TextWithShadow(
            quit_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        quit_surf.draw(
            self.screen.get_width() / 2 - quit_surf.get_width() / 2, 380, self.screen
        )

    def draw_chart_select_menu(self) -> None:
        self.screen.fill(BLACK)
        # -- Update text of the buttons -- #
        chart_texts = []
        for chart_index in range(0, len(self.charts)):
            if chart_index == self.chart_select_menu_selected:
                chart_text = f"> {self.charts[chart_index]} <"
            else:
                chart_text = self.charts[chart_index]
            chart_texts.append(chart_text)

        title_surf = text.TextWithShadow(
            "Charts",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        title_surf.draw(
            self.screen.get_width() / 2 - title_surf.get_width() / 2,
            100,
            self.screen,
        )

        hint_surf = text.TextWithShadow(
            "Press ENTER to select",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        hint_surf.draw(
            self.screen.get_width() / 2 - hint_surf.get_width() / 2,
            self.screen.get_height() - 100,
            self.screen,
        )
        margin = 0
        for chart_text in chart_texts:
            chart_surf = text.TextWithShadow(
                chart_text,
                self.font,
                WHITE,
                BLACK,
                4,
            )
            chart_surf.draw(
                self.screen.get_width() / 2 - chart_surf.get_width() / 2,
                220 + margin,
                self.screen,
            )
            margin += 80

    def draw_difficulty_select_menu(self) -> None:
        self.screen.fill(BLACK)
        # -- Update text of the buttons -- #
        difficulty_texts = []
        for difficulty_index in range(0, len(self.difficulties)):
            if difficulty_index == self.difficulties_select_menu_selected:
                difficulty_text = (
                    f"> {self.difficulties[difficulty_index].difficulty} <"
                )
            else:
                difficulty_text = self.difficulties[difficulty_index].difficulty
            difficulty_texts.append(difficulty_text)

        title_surf = text.TextWithShadow(
            "Difficulties",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        title_surf.draw(
            self.screen.get_width() / 2 - title_surf.get_width() / 2,
            100,
            self.screen,
        )

        hint_surf = text.TextWithShadow(
            "Press ENTER to select",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        hint_surf.draw(
            self.screen.get_width() / 2 - hint_surf.get_width() / 2,
            self.screen.get_height() - 100,
            self.screen,
        )
        margin = 0
        for difficulty_text in difficulty_texts:
            difficulty_surf = text.TextWithShadow(
                difficulty_text,
                self.font,
                WHITE,
                BLACK,
                4,
            )
            difficulty_surf.draw(
                self.screen.get_width() / 2 - difficulty_surf.get_width() / 2,
                220 + margin,
                self.screen,
            )
            margin += 80

    def draw_settings_menu(self) -> None:
        self.screen.fill(BLACK)
        # -- Update text of the buttons -- #
        if self.settings_menu_selected == 0:
            note_speed_text = (
                f"> {self.settings_menu_text[0]}{round(self.settings.note_speed, 1)} <"
            )
        else:
            note_speed_text = (
                f"{self.settings_menu_text[0]}{round(self.settings.note_speed, 1)}"
            )

        if self.settings_menu_selected == 1:
            background_dim_text = (
                f"> {self.settings_menu_text[1]}{self.settings.background_dim}% <"
            )
        else:
            background_dim_text = (
                f"{self.settings_menu_text[1]}{self.settings.background_dim}%"
            )

        if self.settings_menu_selected == 2:
            volume_text = f"> {self.settings_menu_text[2]}{self.settings.volume}% <"
        else:
            volume_text = f"{self.settings_menu_text[2]}{self.settings.volume}%"

        if self.settings_menu_selected == 3:
            back_text = f"> {self.settings_menu_text[3]} <"
        else:
            back_text = f"{self.settings_menu_text[3]}"

        title_surf = text.TextWithShadow(
            "Settings",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        title_surf.draw(
            self.screen.get_width() / 2 - title_surf.get_width() / 2,
            100,
            self.screen,
        )

        note_speed_surf = text.TextWithShadow(
            note_speed_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        note_speed_surf.draw(
            self.screen.get_width() / 2 - note_speed_surf.get_width() / 2,
            220,
            self.screen,
        )

        background_dim_surf = text.TextWithShadow(
            background_dim_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        background_dim_surf.draw(
            self.screen.get_width() / 2 - background_dim_surf.get_width() / 2,
            300,
            self.screen,
        )

        volume_surf = text.TextWithShadow(
            volume_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        volume_surf.draw(
            self.screen.get_width() / 2 - volume_surf.get_width() / 2, 380, self.screen
        )

        back_surf = text.TextWithShadow(
            back_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        back_surf.draw(
            self.screen.get_width() / 2 - back_surf.get_width() / 2,
            460,
            self.screen,
        )

    def draw_pause_menu(self):
        s = pg.Surface(self.size, pg.SRCALPHA)  # per-pixel alpha
        s.fill((0, 0, 0, 128))  # notice the alpha value in the color
        self.screen.blit(s, (0, 0))
        # -- Paused text -- #
        paused_surf = text.TextWithShadow(
            "Game paused",
            self.font,
            WHITE,
            BLACK,
            4,
        )
        paused_surf.draw(
            self.screen.get_width() / 2 - paused_surf.get_width() / 2,
            100,
            self.screen,
        )
        # -- Update text of the buttons -- #
        if self.pause_menu_selected == 0:
            resume_text = f"> {self.pause_menu_text[0]} <"
        else:
            resume_text = self.pause_menu_text[0]

        if self.pause_menu_selected == 1:
            retry_text = f"> {self.pause_menu_text[1]} <"
        else:
            retry_text = self.pause_menu_text[1]

        if self.pause_menu_selected == 2:
            leave_text = f"> {self.pause_menu_text[2]} <"
        else:
            leave_text = self.pause_menu_text[2]

        # -- Buttons -- #
        resume_surf = text.TextWithShadow(
            resume_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        resume_surf.draw(
            self.screen.get_width() / 2 - resume_surf.get_width() / 2, 220, self.screen
        )

        retry_surf = text.TextWithShadow(
            retry_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        retry_surf.draw(
            self.screen.get_width() / 2 - retry_surf.get_width() / 2, 300, self.screen
        )

        leave_surf = text.TextWithShadow(
            leave_text,
            self.font,
            WHITE,
            BLACK,
            4,
        )
        leave_surf.draw(
            self.screen.get_width() / 2 - leave_surf.get_width() / 2, 380, self.screen
        )

    def on_event(self, event) -> None:
        """Used to handle pygame events.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        if event.type == QUIT:
            self._running = False
        if self.game_state == GameState.main_menu:
            self.handle_main_menu(event=event)
        if self.game_state == GameState.chart_select_menu:
            self.handle_chart_select_menu(event=event)
        if self.game_state == GameState.difficulty_select_menu:
            self.handle_difficulty_select_menu(event=event)
        if self.game_state == GameState.paused:
            self.handle_pause_menu(event=event)
        if self.game_state == GameState.settings_menu:
            self.handle_settings_menu(event=event)
        if self.game_state == GameState.in_game:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.audioPlayer.mixer.music.pause()
                    self.game_state = GameState.paused
        if self.game_state == GameState.in_game:
            if event.type == KEYDOWN:
                if event.key == K_EQUALS:
                    self.settings.increment_note_speed()
                    print(self.settings.time_to_react)
                if event.key == K_MINUS:
                    self.settings.decrement_note_speed()
                    print(self.settings.time_to_react)

                if event.key == K_d and not self.pressed_keys[0]:
                    self.handle_note(line=1)
                if event.key == K_f and not self.pressed_keys[1]:
                    self.handle_note(line=2)
                if event.key == K_j and not self.pressed_keys[2]:
                    self.handle_note(line=3)
                if event.key == K_k and not self.pressed_keys[3]:
                    self.handle_note(line=4)

            if event.type == KEYUP:
                if event.key == K_d and self.pressed_keys[0]:
                    self.pressed_keys[0] = False
                if event.key == K_f and self.pressed_keys[1]:
                    self.pressed_keys[1] = False
                if event.key == K_j and self.pressed_keys[2]:
                    self.pressed_keys[2] = False
                if event.key == K_k and self.pressed_keys[3]:
                    self.pressed_keys[3] = False

    def on_loop(self) -> None:
        """Used to perform a game loop."""
        if self.game_state == GameState.in_game:
            self.wait_before_playing_song()
            self.user_interface.update_text(
                self.score, self.lastGrade, self.combo, self.fps
            )
            self.spawn_notes()
            self.update_notes()
            self.update_hits()
            self.update_hit_glows()
            self.audioPlayer.update()

    def on_render(self) -> None:
        """Used to perform rendering on screen."""
        self.clock.tick(FPS)
        if self.game_state == GameState.main_menu:
            self.draw_main_menu()
        if self.game_state == GameState.chart_select_menu:
            self.draw_chart_select_menu()
        if self.game_state == GameState.difficulty_select_menu:
            self.draw_difficulty_select_menu()
        if self.game_state == GameState.settings_menu:
            self.draw_settings_menu()
        if self.game_state == GameState.in_game:
            self.fps = self.clock.get_fps()
            self.screen.fill(BLACK)
            self.other_sprites.draw(self.screen)
            s = pg.Surface(self.size, pg.SRCALPHA)
            s.fill((0, 0, 0, self.backgroundAlpha))
            self.screen.blit(s, (0, 0))
            self.draw_rectangle()
            self.draw_hitbar()
            self.draw_bar()
            self.draw_notes()
            self.user_interface.draw(self.screen)
            for hit in self.all_recent_hits:
                hit.draw(self.screen)
            for hit_glow in self.all_hit_glows:
                hit_glow.draw(self.screen)
                hit_glow.emit(self.screen)
        if self.game_state == GameState.paused:
            self.draw_pause_menu()
        pg.display.update()

    def on_cleanup(self) -> None:
        """Used to handle cleanup when the game is closed."""
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
    # flags = FULLSCREEN | SCALED | HWSURFACE
    flags = RESIZABLE | SCALED
    game = Game(width=1280, height=720, initializationFlags=flags)
    game.on_execute()
