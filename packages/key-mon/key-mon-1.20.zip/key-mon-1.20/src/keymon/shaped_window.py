#!/usr/bin/env python3
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create a shaped window to show mouse events.

Thanks to mathias.gumz for the original code.
"""
import gi

gi.require_version("Gtk", "3.0")
gi.require_foreign("cairo")
from gi.repository import Gtk, Gdk, GLib
import cairo

from . import lazy_pixbuf_creator

class ShapedWindow(Gtk.Window):
  """Create a window shaped as fname."""
  def __init__(self, fname, opacity, color=None, scale=1.0, timeout=0.2):
    Gtk.Window.__init__(self)
    self.connect('size-allocate', self._on_size_allocate)
    self.set_decorated(False)
    self.set_keep_above(True)
    self.set_accept_focus(False)
    self.scale = scale
    self.shown = False
    self.opacity = opacity
    self.timeout = timeout
    self.timeout_timer = None
    self.name_fnames = {
        'mouse' : [fname],
    }
    self.pixbufs = lazy_pixbuf_creator.LazyPixbufCreator(self.name_fnames,
                                                         self.scale,
                                                         color=color)
    self.pixbuf = self.pixbufs.get('mouse')
    self.resize(self.pixbuf.get_width(), self.pixbuf.get_height())

    # a pixmap widget to contain the pixmap
    self.image = Gtk.Image.new_from_pixbuf(self.pixbuf)

    rgba = self.get_screen().get_rgba_visual()
    if rgba is not None:
      self.set_visual(rgba)

    self.set_name("mouse-follow")
    provider = Gtk.CssProvider()
    provider.load_from_data(
        b"""
    #mouse-follow {
        background-color:rgba(0,0,0,0);
    }
    """
    )
    context = self.get_style_context()
    context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    self.image.show()
    self.add(self.image)

  def _on_size_allocate(self, win, unused_allocation):
    """Called when first allocated."""
    # Set the window shape
    win.set_property('skip-taskbar-hint', True)
    if not win.is_composited():
      print('Unable to fade the window')
    else:
      win.set_opacity(self.opacity)

  def center_on_cursor(self, x=None, y=None):
    """Move center of window to the cursor position"""
    if x is None or y is None:
      root = Gdk.Screen.get_default().get_root_window()
      _, x, y, _ = root.get_pointer()
    w, h = self.get_size()
    new_x, new_y = x - w/2, y - h/2
    pos = self.get_position()
    if pos[0] != new_x or pos[1] != new_y or not self.get_visible():
      self.move(new_x, new_y)
      self.show()

  def show(self):
    """Show this mouse indicator and ignore awaiting fade away request."""
    if self.timeout_timer and self.shown:
      # There is a fade away request, ignore it
      if (GLib.main_context_default().find_source_by_id(self.timeout_timer)
          and not GLib.main_context_default().find_source_by_id(self.timeout_timer).is_destroyed()):
        GLib.source_remove(self.timeout_timer)
      self.timeout_timer = None
      # This method only is called when mouse is pressed, so there will be a
      # release and fade_away call, no need to set up another timer.
    super(ShapedWindow, self).show()
    # Fix click-through
    self.input_shape_combine_region(cairo.Region())

  def maybe_show(self):
    """Show the window if not already shown or timer timed out"""
    if self.shown or not self.timeout_timer:
      return
    self.shown = True
    self.show()

  def _end_fade(self):
    self.hide()
    self.timeout_timer = None

  def fade_away(self):
    """Make the window fade in a little bit."""
    # TODO this isn't doing any fading out
    self.shown = False
    self.timeout_timer = GLib.timeout_add(int(self.timeout * 1000), self._end_fade)
