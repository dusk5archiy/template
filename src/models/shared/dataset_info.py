from pydantic import BaseModel

# -----------------------------------------------------------------------------


class ImageProcessingDsInfo(BaseModel):
    colored: bool
    image_resolution: tuple[int, int]  # W x H

    @property
    def num_channels(self):
        return 3 if self.colored else 1


class ClassificationDsInfo(BaseModel):
    num_classes: int


class ImageClassificationDsInfo(ImageProcessingDsInfo, ClassificationDsInfo):
    pass


# -----------------------------------------------------------------------------
