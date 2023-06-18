import pygame as pg
import os
from pygame.locals import *


# imports
import enums
import menu
import audioplayer
import chart
import settings
import performance
import ui
import graphics
import spawner

# Constants
FPS = 1000


class Game:
    """The main class that implements the logic of the game.

    Methods
    -------
    TODO
    """

    def __init__(self, width: int, height: int, initialization_flags) -> None:
        """
        Parameters
        ----------
        width : int
            Screen width.
        height : int
            Screen height.
        initialization_flags : int
            Window initialization flags.

        Raises
        ----------
        AssertionError
            The width or height is not an integer.
        ValueError
            The width or height value is less than zero.
        """
        assert isinstance(width, int), "The width must be an integer."
        assert isinstance(height, int), "The height must be an integer."
        if width <= 0:
            raise ValueError("Width must be greater than zero.")
        if height <= 0:
            raise ValueError("Height must be greater than zero.")

        self.running = True
        self.settings = settings.Settings()
        self._flags = initialization_flags
        self.size = self.width, self.height = width, height

    def on_init(self) -> None:
        """Used to initialize the pygame module, game window and variables."""
        pg.init()
        pg.display.set_caption("Koli Rhythm")
        self.screen = pg.display.set_mode(self.size, self._flags)

        self.load_resources()
        self.initialize_menus()

        self.clock = pg.time.Clock()
        self.audioPlayer = None
        self.game_state = enums.GameState.MAIN_MENU

        self.lastGrade = ""
        self.fps = self.get_fps()
        self.wait_before_playing = 1000
        self.all_recent_hits = []

        self.enter_is_pressed = False
        self.chart_ended = False
        self.started_playing_song = False
        self.pressed_keys = [False, False, False, False]

    def initialize_menus(self) -> None:
        """Used to initialize all menus."""
        self.main_menu = menu.Main(self.font)
        self.settings_menu = menu.Settings(
            self.font,
            self.settings.note_speed,
            self.settings.background_dim,
            self.settings.volume,
            self.settings.username,
        )
        self.charts_menu = menu.Charts(self.font)
        self.pause_menu = menu.Pause(self.font)

    def load_resources(self) -> None:
        """Used to load game resources."""
        self.button_bar = graphics.ButtonBar()
        self.font = pg.font.Font(os.path.join("fonts", "PixeloidSansBold.ttf"), 45)
        self.small_font = pg.font.Font(
            os.path.join("fonts", "PixeloidSansBold.ttf"), 30
        )

    def update_hits(self) -> None:
        """Used to update the transparency of recent hits."""
        for hit in self.all_recent_hits:
            hit.update()
            if hit.ready_to_delete():
                self.all_recent_hits.remove(hit)

    def draw_rectangle(self) -> None:
        """Used to draw two rectangles representing the playing field in the center of the screen."""
        black_surf = pg.Surface((546, self.screen.get_height()))
        black_surf.fill((100, 100, 100))
        white_surf = pg.Surface((558, self.screen.get_height()))
        white_surf.fill(enums.Color.WHITE.value)
        self.screen.blit(
            white_surf,
            (self.screen.get_width() / 2 - white_surf.get_width() / 2, 0),
        )
        self.screen.blit(
            black_surf,
            (self.screen.get_width() / 2 - black_surf.get_width() / 2, 0),
        )

    def update_notes(self) -> None:
        """Used to update the position of notes relative to the audio player's timer."""
        for note in self.notes:
            progress = self.get_note_progress(note)
            note.update_vertical_position(progress)
            if progress >= 0.7:
                note.is_clickable = True
            if progress > 1.3:
                self.performance.max_possible_combo += 1
                if self.performance.combo >= self.performance.max_combo:
                    self.performance.max_combo = self.performance.combo
                self.performance.combo = 0
                self.notes.remove(note)

    def get_note_progress(self, note: graphics.Note) -> float:
        """Used to calculate the progress of a note.

        Parameters
        ----------
        note : Note
            Note object.

        Returns
        ----------
        float
            Calculated note progress.

        Raises
        ----------
        AssertionError
            Note is not an instance of the Note class.
        """
        assert isinstance(
            note, graphics.Note
        ), "Note must be an instance of the Note class."
        progress = 1 - (
            (note.timing + self.wait_before_playing - self.audioPlayer.songPosition)
            / self.settings.time_to_react
        )
        return progress

    def destroy_note(self, line: int) -> None:
        """Used to destroy the note on the desired line.

        Parameters
        ----------
        line : int
            Line number.

        Raises
        ----------
        AssertionError
            The line number is not an integer.
        ValueError
            Line number is less than zero or greater than 4.
        """
        assert isinstance(line, int), "The line number must be an integer."
        if line <= 0 or line > 4:
            raise ValueError(
                "The line number must be greater than zero and less than 4."
            )

        for note in self.notes:
            if note.line == line and note.is_clickable:
                self.performance.max_possible_combo += 1
                self.audioPlayer.hitSound.play()
                self.notes.remove(note)
                break

    def draw_notes(self) -> None:
        """Used to draw notes on screen."""
        for note in self.notes:
            note.draw(self.screen)

    def draw_bar(self) -> None:
        """Used to draw a judgement bar on screen."""
        self.button_bar.draw(self.screen)

    def get_fps(self) -> int:
        """Used to get the current fps.

        Returns
        ----------
        int
            Current fps.
        """
        fps = int(self.clock.get_fps())
        return fps

    def start_playing_song(self) -> None:
        """Used to start playing a song."""
        if not self.started_playing_song:
            self.audioPlayer.play_song()
            self.started_playing_song = True

    def draw_hitbar(self) -> None:
        """Used to draw a hitbar."""
        hitbar = graphics.Hitbar()
        hitbar.draw(self.screen)

    def retry(self) -> None:
        """Used to retry the chart."""
        self.started_playing_song = False
        self.notes.clear()
        self.notes = self.spawner.spawn_notes(self.screen)
        self.performance = performance.Performance(self.settings.username)
        self.audioPlayer = audioplayer.AudioPlayer(
            self.selected_chart.bpm, self.selected_chart.audio
        )
        self.audioPlayer.change_volume(self.settings.volume / 100)
        self.audioPlayer.play_song()
        self.starting_chart_time = pg.time.get_ticks()

    def handle_note(self, line: int) -> None:
        """Used to call functions that depend on the pressed line.

        This function destroys the note on a certain line, updates the performance variables, creates a new hit object, and plays the hit sound.

        Raises
        ----------
        AssertionError
            The line number is not an integer.
        ValueError
            Line number is less than zero or greater than 4.
        """
        assert isinstance(line, int), "The line number must be an integer."
        if line <= 0 or line > 4:
            raise ValueError(
                "The line number must be greater than zero and less than 4."
            )

        note = self.notes[0]
        progress = self.get_note_progress(note)
        self.pressed_keys[line - 1] = True
        self.destroy_note(line)
        self.lastGrade = self.performance.get_grade(progress=progress)
        self.performance.update_accuracy()
        self.performance.add_score(self.lastGrade)
        self.performance.update_combo(self.lastGrade)
        self.performance.update_hits_counter(self.lastGrade)
        hit = graphics.Hit(progress=progress)
        self.all_recent_hits.append(hit)
        self.audioPlayer.hitSound.play()

    def handle_username_input(self, event: pg.event.Event) -> None:
        """Used to handle username input.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.settings.username = self.settings.username[:-1]
            if len(self.settings.username) < 8:
                if event.key == K_SPACE:
                    self.settings.username += "_"
                else:
                    letter = event.unicode
                    if letter.isalpha():
                        self.settings.username += letter

    def handle_main_menu(self, event: pg.event.Event) -> None:
        """Used to handle main menu.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        self.main_menu.update(event=event)
        if event.type == KEYDOWN:
            if event.key == K_RETURN and not self.enter_is_pressed:
                self.enter_is_pressed = True
                selected_button = self.main_menu.get_selected_button()
                if selected_button == 0:
                    self.game_state = enums.GameState.CHART_SELECT_MENU
                    self.charts = self.charts_menu.get_chart_names()
                elif selected_button == 1:
                    self.game_state = enums.GameState.SETTINGS_MENU
                elif selected_button == 2:
                    self.running = False

        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

    def handle_chart_select_menu(self, event: pg.event.Event) -> None:
        """Used to handle chart select menu.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        self.charts_menu.update(event=event)
        if event.type == KEYDOWN:
            if event.key == K_RETURN and not self.enter_is_pressed:
                self.enter_is_pressed = True
                selected_button = self.charts_menu.get_selected_button()
                self.selected_chart = chart.Chart(self.charts[selected_button])
                self.background = graphics.Background(self.selected_chart.background)
                self.background.image = pg.transform.scale(
                    self.background.image, self.size
                )
                self.difficulties_menu = menu.Difficulties(
                    self.font, self.selected_chart
                )
                self.game_state = enums.GameState.DIFFICULTY_SELECT_MENU
            if event.key == K_ESCAPE:
                self.game_state = enums.GameState.MAIN_MENU

        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

    def handle_difficulty_select_menu(self, event: pg.event.Event) -> None:
        """Used to handle difficulty select menu.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        self.difficulties_menu.update(event=event)
        selected_button = self.difficulties_menu.get_selected_button()
        if event.type == KEYDOWN:
            if event.key == K_RETURN and not self.enter_is_pressed:
                self.enter_is_pressed = True
                self.selected_difficulty = self.selected_chart.difficulties[
                    selected_button
                ]
                self.spawner = spawner.Spawner(self.selected_difficulty)
                self.notes = self.spawner.spawn_notes(self.screen)
                self.performance = performance.Performance(
                    player_name=self.settings.username
                )
                self.user_interface = ui.UserInterface(
                    score=self.performance.score,
                    last_grade=self.lastGrade,
                    combo=self.performance.combo,
                    accuracy=self.performance.accuracy,
                    fps=self.fps,
                )
                self.game_state = enums.GameState.PLAYING
                self.audioPlayer = audioplayer.AudioPlayer(
                    self.selected_chart.bpm, self.selected_chart.audio
                )
                self.audioPlayer.change_volume(self.settings.volume / 100)
            if event.key == K_ESCAPE:
                self.game_state = enums.GameState.CHART_SELECT_MENU
        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

    def handle_settings_menu(self, event: pg.event.Event) -> None:
        """Used to handle settings menu.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        self.settings_menu.update(event)
        selected_button = self.settings_menu.get_selected_button()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.game_state = enums.GameState.MAIN_MENU
                self.settings.save()
            if (
                event.key == K_RETURN
                and selected_button == 4
                and not self.enter_is_pressed
            ):
                self.enter_is_pressed = True
                self.settings.save()
                self.game_state = enums.GameState.MAIN_MENU
            if selected_button == 0:
                self.handle_username_input(event=event)

            if event.key == K_LEFT and selected_button == 1:
                self.settings.decrement_note_speed()

            if event.key == K_RIGHT and selected_button == 1:
                self.settings.increment_note_speed()

            if event.key == K_LEFT and selected_button == 2:
                self.settings.decrement_background_dim()

            if event.key == K_RIGHT and selected_button == 2:
                self.settings.increment_background_dim()

            if event.key == K_LEFT and selected_button == 3:
                self.settings.decrement_volume()

            if event.key == K_RIGHT and selected_button == 3:
                self.settings.increment_volume()

        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False
        self.settings_menu.update_text(
            self.settings.note_speed,
            self.settings.background_dim,
            self.settings.volume,
            self.settings.username,
        )

    def handle_pause_menu(self, event: pg.event.Event) -> None:
        """Used to handle pause menu.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        self.pause_menu.update(event)
        selected_button = self.pause_menu.get_selected_button()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.audioPlayer.mixer.music.unpause()
                self.game_state = enums.GameState.PLAYING
            if event.key == K_RETURN and not self.enter_is_pressed:
                self.enter_is_pressed = True
                if selected_button == 0:
                    self.audioPlayer.mixer.music.unpause()
                    self.game_state = enums.GameState.PLAYING
                if selected_button == 1:
                    self.retry()
                    self.game_state = enums.GameState.PLAYING
                if selected_button == 2:
                    self.game_state = enums.GameState.MAIN_MENU
                    self.audioPlayer = None
                    self.started_playing_song = False

        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

    def handle_endscreen(self, event: pg.event.Event) -> None:
        """Used to handle endscreen.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.game_state = enums.GameState.DIFFICULTY_SELECT_MENU

    def handle_gameplay(self, event: pg.event.Event) -> None:
        """Used to handle gameplay.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.audioPlayer.mixer.music.pause()
                self.game_state = enums.GameState.PAUSED

            if event.key == K_EQUALS:
                self.settings.increment_note_speed()

            if event.key == K_MINUS:
                self.settings.decrement_note_speed()

            if event.key == K_d and not self.pressed_keys[0]:
                self.handle_note(line=1)

            if event.key == K_f and not self.pressed_keys[1]:
                self.handle_note(line=2)

            if event.key == K_j and not self.pressed_keys[2]:
                self.handle_note(line=3)

            if event.key == K_k and not self.pressed_keys[3]:
                self.handle_note(line=4)

        if event.type == KEYUP:
            if event.key == K_RETURN:
                self.enter_is_pressed = False

            if event.key == K_d and self.pressed_keys[0]:
                self.pressed_keys[0] = False

            if event.key == K_f and self.pressed_keys[1]:
                self.pressed_keys[1] = False

            if event.key == K_j and self.pressed_keys[2]:
                self.pressed_keys[2] = False

            if event.key == K_k and self.pressed_keys[3]:
                self.pressed_keys[3] = False

    def draw_main_menu(self) -> None:
        """Used to draw the main menu."""
        self.main_menu.draw(self.screen)

    def draw_chart_select_menu(self) -> None:
        """Used to draw the chart select menu."""
        self.charts_menu.draw(self.screen)

    def draw_difficulty_select_menu(self) -> None:
        """Used to draw the difficulty select menu."""
        self.difficulties_menu.draw(self.screen)

    def draw_settings_menu(self) -> None:
        """Used to draw the settings menu."""
        self.settings_menu.draw(self.screen)

    def draw_pause_menu(self):
        """Used to draw the pause menu."""
        self.pause_menu.draw(self.screen)

    def get_last_note_timing(self) -> int:
        """Used to get the timing of the last note in the chart."""
        sorted_notes = list(self.selected_difficulty.notes.items())
        return int(sorted_notes[-1][0])

    def end_of_the_chart(self) -> bool:
        """Used to check the end state of the chart.

        Returns
        ----------
        bool
            Is end of the chart."""
        if self.audioPlayer.songPosition - 3000 > self.get_last_note_timing():
            return True
        return False

    def on_event(self, event: pg.event.Event) -> None:
        """Used to handle pygame events.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.
        """
        if event.type == QUIT:
            self.running = False

        if self.game_state == enums.GameState.MAIN_MENU:
            self.handle_main_menu(event=event)

        if self.game_state == enums.GameState.CHART_SELECT_MENU:
            self.handle_chart_select_menu(event=event)

        if self.game_state == enums.GameState.DIFFICULTY_SELECT_MENU:
            self.handle_difficulty_select_menu(event=event)

        if self.game_state == enums.GameState.PAUSED:
            self.handle_pause_menu(event=event)

        if self.game_state == enums.GameState.SETTINGS_MENU:
            self.handle_settings_menu(event=event)

        if self.game_state == enums.GameState.ENDSCREEN:
            self.handle_endscreen(event=event)

        if self.game_state == enums.GameState.PLAYING:
            self.handle_gameplay(event=event)

    def on_loop(self) -> None:
        """Used to perform a game loop."""
        if self.game_state == enums.GameState.PLAYING:
            if self.end_of_the_chart():
                self.game_state = enums.GameState.ENDSCREEN

            self.start_playing_song()
            self.user_interface.update_text(
                self.performance.score,
                self.lastGrade,
                self.performance.combo,
                self.performance.accuracy,
                int(self.fps),
            )
            self.update_notes()
            self.update_hits()
            self.audioPlayer.update()

    def draw_gameplay(self) -> None:
        """Used to draw chart background, notes and other UI elements."""
        self.fps = self.clock.get_fps()
        self.screen.fill(enums.Color.BLACK.value)
        self.screen.blit(self.background.image, (0, 0))
        dim_surface = pg.Surface(self.size, pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, self.settings.background_alpha))
        self.screen.blit(dim_surface, (0, 0))
        self.draw_rectangle()
        self.draw_hitbar()
        self.draw_bar()
        self.draw_notes()
        self.user_interface.draw(self.screen)
        for hit in self.all_recent_hits:
            hit.draw(self.screen)

    def on_render(self) -> None:
        """Used to perform rendering on screen."""
        self.clock.tick(FPS)
        if self.game_state == enums.GameState.MAIN_MENU:
            self.main_menu.draw(self.screen)

        if self.game_state == enums.GameState.CHART_SELECT_MENU:
            self.charts_menu.draw(self.screen)

        if self.game_state == enums.GameState.DIFFICULTY_SELECT_MENU:
            self.difficulties_menu.draw(self.screen)

        if self.game_state == enums.GameState.SETTINGS_MENU:
            self.settings_menu.draw(self.screen)

        if self.game_state == enums.GameState.ENDSCREEN:
            self.screen.blit(self.background.image, (0, 0))
            self.endscreen = menu.Endscreen(
                self.font, self.small_font, self.performance
            )
            self.endscreen.draw(self.screen)

        if self.game_state == enums.GameState.PLAYING:
            self.draw_gameplay()

        if self.game_state == enums.GameState.PAUSED:
            self.draw_gameplay()
            self.pause_menu.draw(self.screen)

        pg.display.update()

    def on_closure(self) -> None:
        """Used to handle code when the game is closed."""
        self.settings.save()
        pg.quit()

    def on_execute(self) -> None:
        """Used to perform a game logic."""
        if self.on_init() == False:
            self.running = False
        while self.running:
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_closure()


if __name__ == "__main__":
    flags = FULLSCREEN | SCALED | HWSURFACE
    game = Game(width=1280, height=720, initialization_flags=flags)
    game.on_execute()
