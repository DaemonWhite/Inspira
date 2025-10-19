#!@PYTHON@
# inspira.in
#
# Copyright 2025 DaemonWhite
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
import os
import locale
import sys
import signal
import gettext

import config

from config import NAME, VERSION, pkgdatadir, localedir, OS, URI

if "windows" == config.OS:
    path_script = os.path.abspath(sys.argv[0])
    dir_script = os.path.dirname(path_script)
    os.chdir(dir_script)

sys.path.insert(1, config.pkgdatadir)
signal.signal(signal.SIGINT, signal.SIG_DFL)

from inspira.utils import language

## Apply translate 

if "windows" == config.OS:
    gettext_env = language.windows_gettext(locale.getlocale())
    if gettext_env is not None:
        os.environ["LANGUAGE"] = gettext_env[2]
        os.environ["LC_ALL"] = gettext_env[1]
        os.environ["LANG"] = gettext_env[0]
        
        # Installer la traduction Python
        trans = gettext.translation(
            config.NAME, 
            localedir=config.localedir, 
            languages=[gettext_env[0]],
            fallback=True
        )
        trans.install()
        
        # Configuration de libintl pour GTK
        try:
            import ctypes
            libintl = ctypes.cdll.LoadLibrary("libintl-8.dll")
            
            # Convertir les chemins en bytes avec l'encodage approprié
            name_bytes = config.NAME.encode('utf-8')
            localedir_bytes = config.localedir.encode('utf-8')
            utf8_bytes = b'UTF-8'
            
            # Appeler les fonctions de libintl
            libintl.bindtextdomain(name_bytes, localedir_bytes)
            libintl.bind_textdomain_codeset(name_bytes, utf8_bytes)
            libintl.textdomain(name_bytes)
            
        except Exception as e:
            print(f"Warning: Could not configure libintl: {e}", file=sys.stderr)
    else:
        # Pas de traduction disponible, installer une fonction _ basique
        import builtins
        builtins._ = lambda s: s
else:
    # Configuration Unix/Linux
    locale.bindtextdomain(config.NAME, config.localedir)
    locale.textdomain(config.NAME)
    gettext.bindtextdomain(config.NAME, config.localedir)
    gettext.textdomain(config.NAME)
    gettext.install(config.NAME, config.localedir)

if __name__ == '__main__':
    import gi
    from gi.repository import Gio

    resource = Gio.Resource.load(os.path.join(config.pkgdatadir, 'inspira.gresource'))
    resource._register()

    from inspira import main
    sys.exit(main.main(config.VERSION))