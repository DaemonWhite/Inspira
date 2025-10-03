from gi.repository import Adw, Gtk, Gio, GObject

from config import URI_PATH

@Gtk.Template(resource_path=URI_PATH+'/ui/widgets/switch_info_row.ui')
class SwitchInfoRow(Adw.PreferencesRow):
    __gtype_name__ = "SwitchInfoRow"
    __gobject_init__ = "SwitchInfoRow"

    __gsignals__ = {
        'activated': (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    contents = Gtk.Template.Child()

    labels_box = Gtk.Template.Child()
    info_box = Gtk.Template.Child()

    title_label = Gtk.Template.Child()
    subtitle_label = Gtk.Template.Child()

    active_switch = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b = GObject.BindingGroup.new()
        b.bind(
            "action-name",
            self.active_switch,
            "action-name",
            GObject.BindingFlags.SYNC_CREATE
        )
        b.bind(
            "action-target",
            self.active_switch,
            "action-target",
            GObject.BindingFlags.SYNC_CREATE
        )

        self.active_switch.connect(
            "notify::active",
            self.slider_notify_active_cb
        )

        self.demo_group = Gio.SimpleActionGroup()
        self.insert_action_group("row", self.demo_group)
        simple_action = Gio.SimpleAction(name="activated")
        simple_action.connect(
            "activate",
            self.__inverse_switch
        )
        self.demo_group.add_action(simple_action)

    def slider_notify_active_cb(self, widget, param):
        Gtk.Accessible.update_state(
            self, [Gtk.AccessibleState.CHECKED],
            [int(self.active_switch.get_active())]
        )
        self.emit("activated", self)

    def __inverse_switch(self, widget, _):
        state = not self.active_switch.get_active()
        self.active_switch.set_active(state)

    def get_title(self):
        return self.title_label.get_label()

    def get_subtitle(self):
        return self.subtitle_label.get_label()

    def get_active(self):
        return self.active_switch.get_active()

    def set_title(self, title):
        super().set_title(title)
        self.title_label.set_label(title)

    def set_subtitle(self, subtitle):
        if len(subtitle) > 0:
            self.subtitle_label.set_visible(True)
        else:
            self.subtitle_label.set_visible(False)

        self.subtitle_label.set_label(subtitle)

    def set_active(self, active):
        self.active_switch.set_active(active)

    def create_tag(self, name_tag: str):
        label = Gtk.Label()
        label.set_label(name_tag)
        label.add_css_class('tag')
        self.info_box.append(label)
