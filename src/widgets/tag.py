from gi.repository import Gtk, Adw


@Gtk.Template(resource_path='/fr/daemonwhite/Inspira/ui/widgets/tag.ui')
class Tag(Gtk.Box):
    __gtype_name__ = 'Tag'

    tag_name: Gtk.Label = Gtk.Template.Child()
    close: Gtk.Button = Gtk.Template.Child()

    def __init__(self, label: str):
        super().__init__()
        self.tag_name.set_label(label)

