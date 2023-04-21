import terminalio
from adafruit_display_text.label import Label
from displayio import Group

WHITE = 0xFFFFFF
RED = 0xFF0000


class ChoiceMenu:
    selected: int = 0

    def __init__(
        self,
        coord_x: int,
        coord_y: int,
        choices: list,
        group: Group,
        scale: int = 2,
        font: terminalio.FONT = terminalio.FONT,
        highlight: int = RED,
        color: int = WHITE,
        y_interval: int = 26
    ) -> None:
        """
        Initiate a choice menu.
        :param coord_x: X coordinate of the menu.
        :param coord_y: Y coordinate of the menu.
        :param choices: Choices to be displayed.
        :param highlight: Highlight color (when selected).
        :param color: Normal color.
        """
        self.choices_len = len(choices)
        self.group = group
        for index, choice in enumerate(choices, 1):
            self.group.append(
                Label(
                    font=font,
                    scale=scale,
                    text=f"{index}.{choice}",
                    x=coord_x,
                    y=coord_y,
                    color=color
                )
            )
            coord_y += y_interval
        self.group[self.selected].color = highlight

    def select_next(self) -> None:
        self.group[self.selected].color = WHITE
        self.selected = self.selected + 1 if self.selected < self.choices_len - 1 else 0
        self.group[self.selected].color = RED

    def select_previous(self) -> None:
        self.group[self.selected].color = WHITE
        self.selected = self.selected - 1 if self.selected > 0 else self.choices_len - 1
        self.group[self.selected].color = RED
