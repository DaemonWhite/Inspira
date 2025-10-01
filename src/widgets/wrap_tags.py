from gi.repository import Gtk, Adw, GLib

from .tag import Tag


@Gtk.Template(resource_path='/fr/daemonwhite/Inspira/ui/widgets/wrap_tags.ui')
class WrapTags(Adw.WrapBox):
    __gtype_name__ = 'WrapTags'

    def __init__(self,):
        super().__init__()
        self._know_tags = []

    def add_tag(self, tag_name: str):
        tag = Tag(label=tag_name)
        tag.close.connect("clicked", self._remove_tag, tag)
        if tag_name not in self._know_tags and len(tag_name) > 1:
            self.append(tag)
            self._know_tags.append(tag_name)

    def add_tags(self, tags_names: list[str]):
        for tag_name in tags_names:
            self.add_tag(tag_name)

    def _remove_tag(self, _n, tag: Tag):
        tag_name = tag.tag_name.get_label()
        try:
            self._know_tags.remove(tag_name)
        except ValueError as e:
            print(f"WARNING: {e} x={tag.tag_name.get_label()} not exist ")

        self.remove(tag)

    def get_tags(self) -> list[str]:
        return self._know_tags.copy()
