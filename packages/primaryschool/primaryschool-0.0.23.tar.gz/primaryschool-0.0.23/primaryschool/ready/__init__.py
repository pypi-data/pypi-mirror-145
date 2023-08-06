import importlib
import os
import pickle
import threading
from functools import partial
from itertools import zip_longest

import pygame
import pygame_menu
from pygame.locals import *
from pygame_menu._scrollarea import ScrollArea
from pygame_menu.baseimage import BaseImage
from pygame_menu.locals import *
from pygame_menu.widgets import *

from primaryschool.dirs import *
from primaryschool.locale import _
from primaryschool.resource import (
    default_font,
    default_font_path,
    get_default_font,
    get_resource_path,
)
from primaryschool.settings import *
from primaryschool.subjects import subjects
import webbrowser
from primaryschool.dirs import user_screenshot_dir_path
import subprocess

app_description_t = _("app_description_t")


class SaveMenu:
    def __init__(self, ps):
        self.ps = ps
        self.surface = self.ps.surface
        self.title = _("Save game?")
        self._menu = self.ps.get_default_menu(self.title)
        self.save = False

    def add_widgets(self):

        self._menu.add.button(
            _("Save and return"),
            self.save_the_game,
            font_name=self.ps.font_path,
        )
        self._menu.add.button(
            _("Continue"), self.continue_the_game, font_name=self.ps.font_path
        )
        self._menu.add.button(
            _("Return to main menu"),
            self.to_main_menu,
            font_name=self.ps.font_path,
        )

    def to_main_menu(self):
        self.ps.main_menu._menu.full_reset()
        self.ps.main_menu._menu.enable()
        self.ps.main_menu._menu.mainloop(self.surface)

    def save_the_game(self):
        self.ps.subject_game.save(self.ps)
        self._menu.disable()
        self.to_main_menu()

    def continue_the_game(self):
        self._menu.disable()


class ContributorsMenu:
    def __init__(self, ps):
        self.ps = ps
        self.title = _("Contributors & Sponsors")
        self._menu = self.ps.get_default_menu(
            self.title, onclose=pygame_menu.events.EXIT
        )
        self._font = get_default_font(15)
        self._head_font = get_default_font(18)
        self.return_background_color = (200, 200, 255, 200)

    def add_widgets(self):
        contributors_table = self._menu.add.table()
        contributors_table.default_cell_padding = 5
        contributors_table.default_row_background_color = "white"
        contributors_table.add_row(
            [_("Contributors"), _("name"), " ", _("Sponsors"), _("name")],
            cell_font=self._head_font,
        )

        _len = list(range(max(len(app_contributors), len(app_sponsors))))
        for l, c, s in zip_longest(_len, app_contributors, app_sponsors):
            c, s = c or " ", s or " "
            contributors_table.add_row(
                [l + 1, c, " ", l + 1, s], cell_font=self._font
            )

        self._menu.add.button(
            _("Return to main menu"),
            pygame_menu.events.BACK,
            font_name=self.ps.font_path,
            background_color=self.return_background_color,
            float=True,
            align=pygame_menu.locals.ALIGN_RIGHT,
        )


class AboutMenu:
    def __init__(self, ps):

        self.ps = ps
        self.title = _("About")
        self._menu = self.ps.get_default_menu(self.title)
        self.app_name_font = get_default_font(50)
        self.app_version_font = get_default_font(20)
        self.app_description_font = get_default_font(22)
        self.app_url_font = get_default_font(20)
        self.app_author_font = self.app_contributors_font = get_default_font(
            20
        )
        self.contributors_menu = ContributorsMenu(self.ps)
        self._label_font = get_default_font(32)

    def add_widgets(self):
        self._menu.add.label(
            app_name, max_char=-1, font_name=self.app_name_font
        )
        self._menu.add.label(
            app_version, max_char=-1, font_name=self.app_version_font
        )
        self._menu.add.label(
            app_description_t, max_char=-1, font_name=self.app_description_font
        )
        self._menu.add.url(app_url, font_name=self.app_url_font)
        self._menu.add.label(
            _("Author"), max_char=-1, font_name=self._label_font
        )
        self._menu.add.label(
            app_author, max_char=-1, font_name=self.app_author_font
        )

        self.contributors_menu.add_widgets()

        self._menu.add.button(
            _("Contributors & Sponsors"),
            self.contributors_menu._menu,
            font_name=self._label_font,
        )

        self._menu.add.button(
            _("Return to main menu"),
            pygame_menu.events.BACK,
            font_name=self.ps.font_path,
        )


class PlayMenu:
    def __init__(self, ps):
        self.ps = ps
        self.title = _("Play Game")
        self.player_name = self.ps.player_name
        self.player_name_text_input = None
        self._menu = self.ps.get_default_menu(self.title)
        self.subjects = self.ps.subjects
        self.subject_games = self.ps.subject_games
        self.subject_index = self.ps.subject_index = 0
        self.subject_game_index = self.ps.subject_game_index
        self.difficulty_index = self.ps.difficulty_index
        self.subject = self.ps.subject
        self.subject_game = self.ps.subject_game
        self.subject_dropselect = None
        self.subject_game_dropselect = None
        self.difficulty_dropselect = None
        self.continue_button = None
        self.selection_box_bgcolor = (255, 255, 255)
        self.help_lael = None
        self.help_lael_font = get_default_font(20)
        self.esc_lael_font = get_default_font(16)
        self.esc_lael_font.set_bold(True)
        self.help_lael_bg = (228, 0, 252, 30)
        self.help_lael_border_color = (228, 0, 252, 200)

    def set_player_name(self, name):
        self.player_name = self.ps.player_name = name
        if self.player_name_text_input:
            self.player_name_text_input.set_value(self.player_name)

    def get_player_name(self):
        return self.player_name

    def add_widgets(self):
        self.player_name_text_input = self._menu.add.text_input(
            title=_("Name :"),
            default=self.get_player_name(),
            font_name=self.ps.font_path,
        )

        self.subject_dropselect = self._menu.add.dropselect(
            title=_("Subject :"),
            items=[(s.name_t, index) for index, s in enumerate(self.subjects)],
            font_name=self.ps.font_path,
            default=0,
            selection_box_bgcolor=self.selection_box_bgcolor,
            placeholder=_("Select a Subject"),
            onchange=self.on_subject_dropselect_change,
        )
        self.subject_game_dropselect = self._menu.add.dropselect(
            title=_("Game :"),
            items=[
                (g.name_t, index) for index, g in enumerate(self.subject_games)
            ],
            font_name=self.ps.font_path,
            default=0,
            selection_box_bgcolor=self.selection_box_bgcolor,
            placeholder=_("Select a game"),
            onchange=self.on_subject_game_dropselect_change,
        )

        self.difficulty_dropselect = self._menu.add.dropselect(
            title=_("Difficulty :"),
            items=[
                (d, index)
                for index, d in enumerate(self.subject_games[0].difficulties)
            ],
            font_name=self.ps.font_path,
            default=0,
            selection_box_bgcolor=self.selection_box_bgcolor,
            placeholder=_("Select a difficulty"),
            onchange=self.on_difficulty_dropselect_change,
        )
        self.update_selection_box_width()
        self.set_difficulty_index()

        self._menu.add.button(
            _("Play"), self.play_btn_onreturn, font_name=self.ps.font_path
        )

        self.continue_button = self._menu.add.button(
            _("Continue"),
            self.continue_btn_onreturn,
            font_name=self.ps.font_path,
        )
        self.update_continue_button()

        self._menu.add.button(
            _("Return to main menu"),
            pygame_menu.events.BACK,
            font_name=self.ps.font_path,
        )

        self.help_lael = self._menu.add.label(
            "", font_name=self.help_lael_font
        )
        self.update_help_lael()

        self._menu.add.label(
            _("After starting the game, press ESC to return."),
            font_name=self.esc_lael_font,
            font_color=(255, 0, 0),
        )

    def update_selection_box_width(self):
        for ds in [
            self.subject_dropselect,
            self.subject_game_dropselect,
            self.difficulty_dropselect,
        ]:

            ds._selection_box_width = (
                max([b.get_width() for b in ds._option_buttons])
                + ds._selection_box_inflate[0]
            )
            ds._make_selection_drop()
            ds.render()

    def play_btn_onreturn(self):
        self.start_the_game()

    def continue_btn_onreturn(self):
        self.start_copied_game()

    def update_continue_button(self):
        if self.subject_game.has_copy():
            self.continue_button.show()
        else:
            self.continue_button.hide()

    def update_subject_game_dropselect(self):
        self.subject_game_dropselect.update_items(
            [(g.name_t, index) for index, g in enumerate(self.subject.games)]
        )
        self.subject_game_dropselect.set_value(self.subject_game_index)

    def update_difficulty_dropselect(self):
        self.difficulty_dropselect.update_items(
            [
                (d, index)
                for index, d in enumerate(self.subject_game.difficulties)
            ]
        )
        self.difficulty_dropselect.set_value(self.difficulty_index)

    def update_help_lael(self):
        self.help_lael.set_title(self.subject_game.help_t.strip())
        self.help_lael.set_background_color(self.help_lael_bg)
        self.help_lael.set_border(2, self.help_lael_border_color)

    def start_copied_game(self):
        self.subject_game.load(self.ps)

    def start_the_game(self):
        self.subject_game.play(self.ps)

    def on_difficulty_dropselect_change(self, value, index):
        self.set_difficulty_index(index)

    def on_subject_dropselect_change(self, item, index):
        self.set_subject_index(index)

    def on_subject_game_dropselect_change(self, item, index):
        self.set_subject_game_index(index)

    def set_subject_index(self, index=0):
        self.subject_index = self.ps.subject_index = index
        self.subject = self.ps.subject = self.subjects[self.subject_index]
        self.subject_games = self.ps.subject_games = self.subject.games
        self.set_subject_game_index()
        self.update_subject_game_dropselect()
        self.update_selection_box_width()

    def set_subject_game_index(self, index=0):
        self.subject_game_index = self.ps.subject_game_index = index
        self.subject_game = self.ps.subject_game = self.subject.games[
            self.subject_game_index
        ]
        self.update_continue_button()
        self.set_difficulty_index()
        self.update_help_lael()

    def set_difficulty_index(self, index=0):
        self.difficulty_index = self.ps.difficulty_index = (
            index if index != 0 else self.subject_game.default_difficulty_index
        )
        self.update_difficulty_dropselect()


class MainMenu:
    def __init__(self, ps):
        self.ps = ps
        self.title = _("Primary School")
        self._menu = self.ps.get_default_menu(self.title)
        self.play_menu = self.ps.play_menu
        self.about_menu = self.ps.about_menu

    def open_screenshots_dir(self):
        _open = (
            sys.platform == "darwin"
            and "open"
            or sys.platform == "win32"
            and "explorer"
            or "xdg-open"
        )
        subprocess.Popen([_open, user_screenshot_dir_path])

    def add_widgets(self):
        self._menu.add.button(
            _("Play"),
            self.ps.play_menu._menu,
            font_name=self.ps.font_path,
        )
        self._menu.add.button(
            _("About"),
            self.ps.about_menu._menu,
            font_name=self.ps.font_path,
        )
        self._menu.add.button(
            _("Quit"),
            pygame_menu.events.EXIT,
            font_name=self.ps.font_path,
        )
        self._menu.add.button(
            _("Screenshots"),
            self.open_screenshots_dir,
            font_name=self.ps.font_path,
            align=pygame_menu.locals.ALIGN_RIGHT,
            background_color=(100, 20, 20, 50),
            font_color=(20, 20, 100),
        )


class PrimarySchool:
    def __init__(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w_width, self.w_height = self.surface.get_size()
        self.w_width_of_2 = self.w_width / 2
        self.w_height_of_2 = self.w_height / 2
        self.w_centrex_y = [self.w_width_of_2, self.w_height]
        self.FPS = 30
        self.player_name = _("default_name")
        self.clock = pygame.time.Clock()
        self.subjects = subjects
        self.subject_games = self.subjects[0].games
        self.subject_index = 0
        self.subject_game_index = 0
        self.difficulty_index = 0
        self.subject = self.subjects[0]
        self.subject_game = self.subject_games[0]
        self.font_path = default_font_path
        self.font = default_font
        self.bg_img = None
        self.play_menu = PlayMenu(self)
        self.about_menu = AboutMenu(self)
        self.save_menu = SaveMenu(self)
        self.main_menu = MainMenu(self)

    def add_widgets(self):
        self.play_menu.add_widgets()
        self.about_menu.add_widgets()
        self.save_menu.add_widgets()
        self.main_menu.add_widgets()

    def set_bg_img(self, src_name="0x1.png"):
        self.bg_img = BaseImage(
            get_resource_path(src_name), pygame_menu.baseimage.IMAGE_MODE_FILL
        )

    def get_bg_img(self):
        if not self.bg_img:
            self.set_bg_img()
        return self.bg_img

    def get_default_menu(self, title, **kwargs):
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.title_font = theme.widget_font = self.font
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        theme.background_color = self.get_bg_img()
        return pygame_menu.Menu(
            title, self.w_width, self.w_height, theme=theme, **kwargs
        )

    def clear_screen(self):
        self.surface.fill((255, 255, 255))
        pygame.display.update()

    def run(self):

        self.add_widgets()

        while self.running:
            self.clock.tick(self.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if self.main_menu._menu.is_enabled():
                self.main_menu._menu.mainloop(self.surface)

            pygame.display.flip()


def go():
    PrimarySchool().run()
    pass
