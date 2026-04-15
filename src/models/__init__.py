from .resnet import Resnet
from .mobilenet import Mobilenet
from .score01 import Score01

CUSTOM_OBJECTS = {
    cls.__name__: cls
    for cls in [
        Resnet,
        Mobilenet,
        Score01,
    ]
}
