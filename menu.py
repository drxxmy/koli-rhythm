import os
import pygame as pg
from abc import ABC, abstractmethod
import chart
import enums
import text
import performance
from pygame.locals import *


class Menu(ABC):
    """The abstract class used to represent a menu.

    Methods
    -------
    get_formated_buttons()
        Used to get formated button texts.
    get_selected_button()
        Used to get selected button number.
    update(event)
        Used to update menu.
    draw(screen)
        Used to draw menu on screen.
    """

    @abstractmethod
    def __init__(self, font: pg.font.Font) -> None:
        """
        Parameters
        ----------
        font : pg.font.Font
            Pygame font.

        Raises
        ------
        AssertionError
            font is not an instance of the pg.font.Font class.
        """
        assert isinstance(
            font, pg.font.Font
        ), "font must be an instance of the pg.font.Font class."
        self.buttons_text = []
        self.selected_button = 0
        self.font = font
        self.pressed_enter = False

    @abstractmethod
    def get_formated_buttons(self) -> list:
        """Used to get formated button texts.

        Returns
        ----------
        list
            List of formated button texts.
        """
        pass

    @abstractmethod
    def get_selected_button(self) -> int:
        """Used to get selected button number.

        Returns
        ----------
        int
            Number of the selected button.
        """
        pass

    @abstractmethod
    def update(self, event: pg.event.Event) -> None:
        """Used to update menu.

        Parameters
        ----------
        event : pg.event.Event
            Pygame event.

        Raises
        ------
        AssertionError
            event is not an instance of the pg.event.Event class.
        """
        assert isinstance(
            event, pg.event.Event
        ), "event must be an instance of the pg.event.Event class."

    @abstractmethod
    def draw(self, screen: pg.surface.Surface) -> None:
        """Used to draw menu on screen.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.

        Raises
        ------
        AssertionError
            screen is not an instance of the pg.surface.Surface class.
        """
        assert isinstance(
            screen, pg.surface.Surface
        ), "screen must be an instance of the pg.surface.Surface class."


class Main(Menu):
    """The class used to represent a main menu.

    Methods
    -------
    get_formated_buttons()
        Used to get formated button texts.
    get_selected_button()
        Used to get selected button number.
    update(event)
        Used to update menu.
    draw(screen)
        Used to draw menu on screen.
    """

    def __init__(self, font: pg.font.Font) -> None:
        super().__init__(font)
        self.buttons = ["Play", "Settings", "Quit"]

    def get_formated_buttons(self) -> list:
        formated_buttons = []
        for button in self.buttons:
            button_index = self.buttons.index(button)
            if button_index == self.selected_button:
                formated_button = f"> {self.buttons[button_index]} <"
                formated_buttons.append(formated_button)
            else:
                formated_buttons.append(button)
        return formated_buttons

    def get_selected_button(self) -> int:
        return self.selected_button

    def update(self, event: pg.event.Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.selected_button < len(self.buttons) - 1:
                    self.selected_button += 1
                else:
                    self.selected_button = 0
            if event.key == K_UP:
                if self.selected_button > 0:
                    self.selected_button -= 1
                else:
                    self.selected_button = len(self.buttons) - 1

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        surface = text.TextWithShadow(
            "Koli Rhythm",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            100,
            screen,
        )

        formated_buttons = self.get_formated_buttons()
        offset = 0

        for button in formated_buttons:
            surface = text.TextWithShadow(
                button, self.font, enums.Color.WHITE.value, enums.Color.BLACK.value, 4
            )
            surface.draw(
                screen.get_width() / 2 - surface.get_width() / 2, 220 + offset, screen
            )
            offset += 80


class Charts(Menu):
    """The class used to represent a chart select menu.

    Methods
    -------
    get_chart_names()
        Used to get chart names.
    get_formated_buttons()
        Used to get formated button texts.
    get_selected_button()
        Used to get selected button number.
    update(event)
        Used to update menu.
    draw(screen)
        Used to draw menu on screen.
    """

    def __init__(self, font: pg.font.Font) -> None:
        super().__init__(font)
        self.buttons = self.get_chart_names()
        self.selected_button = 0

    def get_chart_names(self) -> list:
        """Used to get chart names.

        Returns
        ----------
        list
            List of chart names.
        """
        chart_names = [
            f.name for f in os.scandir(os.path.join("src", "charts")) if f.is_dir()
        ]
        return chart_names

    def get_formated_buttons(self) -> list:
        formated_buttons = []
        for button in self.buttons:
            button_index = self.buttons.index(button)
            if button_index == self.selected_button:
                formated_button = f"> {self.buttons[button_index]} <"
                formated_buttons.append(formated_button)
            else:
                formated_buttons.append(button)
        return formated_buttons

    def get_selected_button(self) -> int:
        return self.selected_button

    def update(self, event: pg.event.Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.selected_button < len(self.buttons) - 1:
                    self.selected_button += 1
                else:
                    self.selected_button = 0
            if event.key == K_UP:
                if self.selected_button > 0:
                    self.selected_button -= 1
                else:
                    self.selected_button = len(self.buttons) - 1

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        surface = text.TextWithShadow(
            "Charts",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            100,
            screen,
        )

        formated_buttons = self.get_formated_buttons()
        offset = 0

        for button in formated_buttons:
            surface = text.TextWithShadow(
                button, self.font, enums.Color.WHITE.value, enums.Color.BLACK.value, 4
            )
            surface.draw(
                screen.get_width() / 2 - surface.get_width() / 2, 220 + offset, screen
            )
            offset += 80


class Difficulties(Menu):
    """The class used to represent a difficulty select menu.

    Methods
    -------
    get_formated_buttons()
        Used to get formated button texts.
    get_selected_button()
        Used to get selected button number.
    update(event)
        Used to update menu.
    draw(screen)
        Used to draw menu on screen.
    """

    def __init__(self, font: pg.font.Font, chart: chart.Chart) -> None:
        """
        Parameters
        ----------
        font : pg.font.Font
            Pygame font.
        chart : chart.Chart
            Selected chart.

        Raises
        ------
        AssertionError
            font is not an instance of the pg.font.Font class.
        """
        super().__init__(font)
        self.buttons = chart.get_difficulty_names()
        self.selected_button = 0

    def get_formated_buttons(self) -> list:
        formated_buttons = []
        for button in self.buttons:
            button_index = self.buttons.index(button)
            if button_index == self.selected_button:
                formated_button = f"> {self.buttons[button_index]} <"
                formated_buttons.append(formated_button)
            else:
                formated_buttons.append(button)
        return formated_buttons

    def get_selected_button(self) -> int:
        return self.selected_button

    def update(self, event: pg.event.Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.selected_button < len(self.buttons) - 1:
                    self.selected_button += 1
                else:
                    self.selected_button = 0
            if event.key == K_UP:
                if self.selected_button > 0:
                    self.selected_button -= 1
                else:
                    self.selected_button = len(self.buttons) - 1

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        surface = text.TextWithShadow(
            "Difficulties",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            100,
            screen,
        )

        surface = text.TextWithShadow(
            "Press ENTER to select",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            screen.get_height() - 100,
            screen,
        )

        formated_buttons = self.get_formated_buttons()
        offset = 0

        for button in formated_buttons:
            surface = text.TextWithShadow(
                button, self.font, enums.Color.WHITE.value, enums.Color.BLACK.value, 4
            )
            surface.draw(
                screen.get_width() / 2 - surface.get_width() / 2, 220 + offset, screen
            )
            offset += 80


class Pause(Menu):
    """The class used to represent a chart select menu.

    Methods
    -------
    get_formated_buttons()
        Used to get formated button texts.
    get_selected_button()
        Used to get selected button number.
    update(event)
        Used to update menu.
    draw(screen)
        Used to draw menu on screen.
    """

    def __init__(self, font: pg.font.Font) -> None:
        super().__init__(font)
        self.buttons = ["Resume", "Retry", "Leave"]
        self.selected_button = 0

    def get_formated_buttons(self) -> list:
        formated_buttons = []
        for button in self.buttons:
            button_index = self.buttons.index(button)
            if button_index == self.selected_button:
                formated_button = f"> {self.buttons[button_index]} <"
                formated_buttons.append(formated_button)
            else:
                formated_buttons.append(button)
        return formated_buttons

    def get_selected_button(self) -> int:
        return self.selected_button

    def update(self, event: pg.event.Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.selected_button < len(self.buttons) - 1:
                    self.selected_button += 1
                else:
                    self.selected_button = 0
            if event.key == K_UP:
                if self.selected_button > 0:
                    self.selected_button -= 1
                else:
                    self.selected_button = len(self.buttons) - 1

    def draw(self, screen: pg.surface.Surface) -> None:
        dim_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 200))
        screen.blit(dim_surface, (0, 0))
        surface = text.TextWithShadow(
            "Game paused",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            100,
            screen,
        )

        formated_buttons = self.get_formated_buttons()
        offset = 0

        for button in formated_buttons:
            surface = text.TextWithShadow(
                button, self.font, enums.Color.WHITE.value, enums.Color.BLACK.value, 4
            )
            surface.draw(
                screen.get_width() / 2 - surface.get_width() / 2, 220 + offset, screen
            )
            offset += 80


class Settings(Menu):
    """The class used to represent a settings menu.

    Methods
    -------
    get_formated_buttons()
        Used to get formated button texts.
    update_text(note_speed, background_dim, volume, username)
        Used to update menu text.
    get_selected_button()
        Used to get selected button number.
    format_username()
        Used to format username.
    update(event)
        Used to update menu.
    draw(screen)
        Used to draw menu on screen.
    """

    def __init__(
        self,
        font: pg.font.Font,
        note_speed: float,
        background_dim: int,
        volume: int,
        username: str,
    ) -> None:
        """
        Parameters
        ----------
        font : pg.font.Font
            Pygame font.
        note_speed : float
            Speed of the note.
        background_dim : int
            Background dim.
        volume : int
            Volume of the music.
        username : str
            Player username.

        Raises
        ------
        AssertionError
            font is not an instance of the pg.font.Font class.
        AssertionError
            note_speed is not a float.
        AssertionError
            background_dim is not an integer.
        AssertionError
            volume is not an integer.
        AssertionError
            username is not a string
        """
        assert isinstance(note_speed, float), "note_speed must be a float."
        assert isinstance(background_dim, int), "background_dim must be an integer."
        assert isinstance(volume, int), "volume must be an integer."
        assert isinstance(username, str), "username must be a string."
        super().__init__(font)
        self.buttons = [
            f"Note Speed: {round(note_speed, 1)}",
            f"Background Dim: {background_dim}",
            f"Volume: {volume}",
            "Back",
        ]
        self.buttons.insert(0, self.format_username(username))
        self.selected_button = 0

    def get_formated_buttons(self) -> list:
        formated_buttons = []
        for button in self.buttons:
            button_index = self.buttons.index(button)
            if button_index == self.selected_button:
                formated_button = f"> {self.buttons[button_index]} <"
                formated_buttons.append(formated_button)
            else:
                formated_buttons.append(button)
        return formated_buttons

    def update_text(
        self, note_speed: float, background_dim: int, volume: int, username: str
    ):
        """Used to update menu text.

        Parameters
        ----------
        note_speed : float
            Speed of the note.
        background_dim : int
            Background dim.
        volume : int
            Volume of the music.
        username : str
            Player username.

        Returns
        ----------
        list
            List of chart names.

        Raises
        ------
        AssertionError
            note_speed is not a float.
        AssertionError
            background_dim is not an integer.
        AssertionError
            volume is not an integer.
        AssertionError
            username is not a string.
        """
        assert isinstance(note_speed, float), "note_speed must be a float."
        assert isinstance(background_dim, int), "background_dim must be an integer."
        assert isinstance(volume, int), "volume must be an integer."
        assert isinstance(username, str), "username must be a string."
        self.buttons.clear()
        self.buttons = [
            f"Note Speed: {round(note_speed, 1)}",
            f"Background Dim: {background_dim}",
            f"Volume: {volume}",
            "Back",
        ]
        self.buttons.insert(0, self.format_username(username))

    def get_selected_button(self) -> int:
        return self.selected_button

    def format_username(self, username: str) -> str:
        """Used to format username.

        Parameters
        ----------
        username : str
            Player username.

        Returns
        ----------
        str
            Formated username.

        Raises
        ------
        AssertionError
            username is not a string.
        """
        assert isinstance(username, str), "username must be a string."
        if len(username) < 8:
            username = username + (8 - len(username)) * "_"
        else:
            username = username
        username = username.replace(" ", "_")
        return username

    def update(self, event: pg.event.Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.selected_button < len(self.buttons) - 1:
                    self.selected_button += 1
                else:
                    self.selected_button = 0
            if event.key == K_UP:
                if self.selected_button > 0:
                    self.selected_button -= 1
                else:
                    self.selected_button = len(self.buttons) - 1

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        surface = text.TextWithShadow(
            "Settings",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            100,
            screen,
        )

        formated_buttons = self.get_formated_buttons()
        offset = 0

        for button in formated_buttons:
            surface = text.TextWithShadow(
                button, self.font, enums.Color.WHITE.value, enums.Color.BLACK.value, 4
            )
            surface.draw(
                screen.get_width() / 2 - surface.get_width() / 2, 220 + offset, screen
            )
            offset += 80


class Endscreen:
    """The class used to represent an Endscreen.

    Methods
    -------
    draw(screen)
        Used to draw menu on screen.
    """

    def __init__(
        self,
        font: pg.font.Font,
        small_font: pg.font.Font,
        performance: performance.Performance,
    ) -> None:
        """
        Parameters
        ----------
        font : pg.font.Font
            Pygame font.
        small_font : pg.font.Font
            Pygame font.
        performance : performance.Performance
            Player's performance.

        Raises
        ------
        AssertionError
            font is not an instance of the pg.font.Font class.
        AssertionError
            small_font is not an instance of the pg.font.Font class.
        AssertionError
            performance is not an instance of the performance.Performance class.
        """
        assert isinstance(
            small_font, pg.font.Font
        ), "small_font must be an instance of the pg.font.Font class."
        assert isinstance(
            performance, performance.Performance
        ), "performance must be an instance of the performance.Performance class."
        self.font = font
        self.small_font = small_font
        self.data = [
            "Result",
            f"Score: {performance.score:,d}",
            f"Combo: {performance.max_combo:,d}/{performance.max_possible_combo:,d}",
            f"Accuracy: {round(performance.accuracy, 2)}%",
            f"Perfect: {performance.perfect_hits} | Good: {performance.good_hits} | Bad: {performance.bad_hits} | Miss: {performance.misses}",
        ]

    def draw(self, screen: pg.surface.Surface) -> None:
        """Used to draw endscreen on screen.

        Parameters
        ----------
        screen : pg.surface.Surface
            Display surface.
        """
        dim_surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 200))
        screen.blit(dim_surface, (0, 0))
        offset = 0

        for surface_text in self.data:
            if self.data.index(surface_text) == 4:
                surface = text.TextWithShadow(
                    surface_text,
                    self.small_font,
                    enums.Color.WHITE.value,
                    enums.Color.BLACK.value,
                    4,
                )
                surface.draw(
                    screen.get_width() / 2 - surface.get_width() / 2,
                    100 + offset,
                    screen,
                )
                offset += 100
            else:
                surface = text.TextWithShadow(
                    surface_text,
                    self.font,
                    enums.Color.WHITE.value,
                    enums.Color.BLACK.value,
                    4,
                )
                surface.draw(
                    screen.get_width() / 2 - surface.get_width() / 2,
                    100 + offset,
                    screen,
                )
                offset += 100

        surface = text.TextWithShadow(
            "Press ESCAPE to close endscreen",
            self.font,
            enums.Color.WHITE.value,
            enums.Color.BLACK.value,
            4,
        )
        surface.draw(
            screen.get_width() / 2 - surface.get_width() / 2,
            screen.get_height() - 100,
            screen,
        )
