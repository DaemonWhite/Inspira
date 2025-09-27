# main.py
#
# Copyright 2025 Mathéo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import InspiraWindow

from .core.manager import Manager

from config import VERSION, NAME, pkgdatadir
from .utils.load_apis import load_apis

class InspiraApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='fr.daemonwhite.Inspira',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/fr/daemonwhite/Inspira')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

        self.win = None
        self.manager = Manager()
        self.load_apis()

    def load_apis(self):
        apis = load_apis(f"{pkgdatadir}/{NAME}/apis", NAME)

        for api in apis:
            self.manager.register(api, True)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = InspiraWindow(application=self)
        self.win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name=NAME,
                                application_icon='fr.daemonwhite.Inspira',
                                developer_name='DaemonWhite',
                                version=VERSION,
                                developers=['DaemonWhite'],
                                copyright='© 2025 DaemonWhite')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = InspiraApplication()
    return app.run(sys.argv)
