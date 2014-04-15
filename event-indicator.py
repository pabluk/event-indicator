#!/usr/bin/env python
#
# Copyright 2012 Pablo SEMINARIO
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of either or both of the following licenses:
#
# 1) the GNU Lesser General Public License version 3, as published by the
# Free Software Foundation; and/or
# 2) the GNU Lesser General Public License version 2.1, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the applicable version of the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of both the GNU Lesser General Public
# License version 3 and version 2.1 along with this program.  If not, see
# <http://www.gnu.org/licenses/>
#
import os.path
import pickle
from datetime import datetime

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


STATE_FILE = os.path.join(os.path.expanduser("~"),
                          ".cache", "event-indicator.dat")

EVENT_START = 'start'
EVENT_STOP = 'stop'


class EventIndicator(object):

    def __init__(self):
        self.event_list = []
        self.load_state()
        self.indicator = appindicator.Indicator.new(
            "event-indicator",
            "user-idle-panel",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.generate_menu()
        Gtk.main()

    def on_event_activate(self, widget, event_type):
        print(event_type)
        self.event_list.append((datetime.now(), event_type))
        self.generate_menu()
        self.save_state()

    def on_clear_activate(self, widget):
        print("Clearing list...")
        self.event_list = []
        self.generate_menu()
        self.save_state()

    def on_quit_activate(self, widget):
        print("Bye!")
        Gtk.main_quit()

    def generate_menu(self):
        print("Generating menu...")
        menu = Gtk.Menu()

        item = Gtk.MenuItem("Start event")
        item.connect("activate", self.on_event_activate, EVENT_START)
        menu.append(item)

        item = Gtk.MenuItem("Stop event")
        item.connect("activate", self.on_event_activate, EVENT_STOP)
        menu.append(item)

        item = Gtk.SeparatorMenuItem()
        menu.append(item)

        if self.event_list:
            for event_time, event_type in self.event_list:
                label = "%s %s" % (event_time.strftime("%H:%M:%S"), event_type)
                print("adding item %s" % label)
                item = Gtk.MenuItem(label)
                menu.append(item)
            item = Gtk.SeparatorMenuItem()
            menu.append(item)

        item = Gtk.MenuItem("Clear events")
        item.connect("activate", self.on_clear_activate)
        menu.append(item)

        item = Gtk.SeparatorMenuItem()
        menu.append(item)

        item = Gtk.MenuItem("Quit")
        item.connect("activate", self.on_quit_activate)
        menu.append(item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def save_state(self):
        print("saving event list")
        pickle.dump(self.event_list, open(STATE_FILE, 'wb'))

    def load_state(self):
        try:
            self.event_list = pickle.load(open(STATE_FILE, 'rb'))
        except IOError:
            self.event_list = []


if __name__ == "__main__":
    indicator = EventIndicator()
