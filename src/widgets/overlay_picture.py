from gi.repository import Gtk, GLib, Gdk

from ..core.imgData import ImgData


@Gtk.Template(resource_path='/fr/daemonwhite/Inspira/ui/widgets/overlay_picture.ui')
class OverlayPicture(Gtk.Overlay):
    __gtype_name__ = "OverlayPicture"

    image: Gtk.Picture = Gtk.Template.Child()
    main_overlay: Gtk.Box = Gtk.Template.Child()
    download: Gtk.Button = Gtk.Template.Child()
    info: Gtk.Button = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.__image: ImgData = None

        self.download.connect("clicked", lambda _: self.save_image())

    def set_image(self, image_data: ImgData):
        bytes_data = GLib.Bytes.new(image_data.img)
        texture = Gdk.Texture.new_from_bytes(bytes_data)
        self.__image = image_data
        self.image.set_paintable(texture)

    def save_image(self):
        if self.__image is None:
            return

        file_dialog = Gtk.FileDialog()
        file_dialog.set_initial_name("image.png")
        file_dialog.save(self.get_root(), None, self.on_save_response)

    def on_save_response(self, dialog, res):
        try:
            file = dialog.save_finish(res)
            if file:
                path = file.get_path()
                if path:
                    with open(path, "wb") as f:
                        f.write(self.__image.img)
                    print(f"Img save in {path}")
        except Exception as e:
            print("Save cancel or error :", e)
