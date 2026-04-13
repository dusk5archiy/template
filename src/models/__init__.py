from .resnet import Resnet
from .mobilenet import Mobilenet

CUSTOM_OBJECTS = {
    cls.__name__: cls
    for cls in [
        Resnet,
        Mobilenet,
    ]
}
