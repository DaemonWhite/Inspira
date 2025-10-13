from gi.repository import GObject
from ..core.Api.imgData import ImgData


class ImageItem(GObject.GObject):
    data = GObject.Property(type=object)

    def __init__(self, data: ImgData):
        super().__init__()
        self.data = data
