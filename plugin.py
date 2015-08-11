# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Thomas Amland
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import xbmc
import xbmcvfs
import routing
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory
from urllib import urlencode, quote_plus


plugin = routing.Plugin()


@plugin.route("/")
def root():
    return


@plugin.route("/browse")
def path_browser():
    args = plugin.args
    current_path = args['path'][0]
    if not current_path.endswith('/'):
        current_path += '/'

    dirs = []
    files = []
    if xbmcvfs.exists(current_path):
        dirs, files = xbmcvfs.listdir(current_path)

    for name in dirs:
        li = ListItem(name)
        if 'fanart' in args:
            li.setArt({'fanart': args['fanart'][0]})
        path = os.path.join(current_path, name)
        params = {
            b'path': path,
            b'title': args['title'][0],
            b'fanart': args['fanart'][0],
        }
        url = 'plugin://context.item.extras/browse?' + urlencode(params)
        addDirectoryItem(plugin.handle, url, li, isFolder=True)

    for name in files:
        li = ListItem(name)
        if 'fanart' in args:
            li.setArt({'fanart': args['fanart'][0]})
        url = os.path.join(current_path, name)
        addDirectoryItem(plugin.handle, url, li, isFolder=False)

    endOfDirectory(plugin.handle)


if __name__ == '__main__':
    plugin.run()
