import enum


class ModelName(str, enum.Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
