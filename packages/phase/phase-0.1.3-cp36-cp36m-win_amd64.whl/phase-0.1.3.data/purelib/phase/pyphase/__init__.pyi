"""
        pyPhase is a python wrapper package over I3DR's Phase C++ library.
    """
import phase.pyphase
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "RGBDVideoStream",
    "RGBDVideoWriter",
    "StereoVision",
    "bgr2bgra",
    "bgr2rgba",
    "bgra2rgba",
    "calib",
    "cvMatIsEqual",
    "depth2xyz",
    "disparity2depth",
    "disparity2xyz",
    "flip",
    "getVersionMajor",
    "getVersionMinor",
    "getVersionPatch",
    "getVersionString",
    "normaliseDisparity",
    "processStereo",
    "processStereoFiles",
    "readImage",
    "savePLY",
    "scaleImage",
    "showImage",
    "stereocamera",
    "stereomatcher",
    "types",
    "xyz2depth"
]


class RGBDVideoStream():
    """
    RGBD Video Stream


    Stream RGB and Depth video
    """
    def __init__(self, arg0: str, arg1: str) -> None: ...
    def close(self) -> None: ...
    def getDownsampleFactor(self) -> float: ...
    def getHFOV(self) -> float: ...
    def getHeight(self) -> int: ...
    def getLoadThreadResult(self) -> bool: ...
    @staticmethod
    def getReadThreadResult(*args, **kwargs) -> typing.Any: ...
    def getWidth(self) -> int: ...
    def isFinished(self) -> bool: ...
    def isLoadThreadRunning(self) -> bool: ...
    def isLoaded(self) -> bool: ...
    def isOpened(self) -> bool: ...
    def isReadThreadRunning(self) -> bool: ...
    def load(self) -> bool: ...
    def loadThreaded(self) -> None: ...
    @staticmethod
    def read(*args, **kwargs) -> typing.Any: ...
    def readThreaded(self) -> None: ...
    def restart(self) -> None: ...
    def setDownsampleFactor(self, arg0: float) -> None: ...
    pass
class RGBDVideoWriter():
    """
    RGBD Video Writer


    Write RGB and Depth video
    """
    def __init__(self, arg0: str, arg1: str, arg2: int, arg3: int) -> None: ...
    def add(self, arg0: numpy.ndarray, arg1: numpy.ndarray) -> None: ...
    def close(self) -> None: ...
    def getSaveThreadResult(self) -> bool: ...
    def isOpened(self) -> bool: ...
    def isSaveThreadRunning(self) -> bool: ...
    def save(self) -> bool: ...
    def saveThreaded(self) -> None: ...
    pass
class StereoVision():
    """
    Stereo Vision class


    Capture images from stereo camera and process with stereo matcher
    to generate depth. Brings together Stereo Camera and Stereo Matcher classes into
    single class for easy use.
    """
    @staticmethod
    def __init__(*args, **kwargs) -> typing.Any: ...
    def connect(self) -> bool: ...
    def disconnect(self) -> None: ...
    @staticmethod
    def getCalibration(*args, **kwargs) -> typing.Any: ...
    @staticmethod
    def getCamera(*args, **kwargs) -> typing.Any: ...
    def getDownsampleFactor(self) -> float: ...
    def getHFOV(self) -> float: ...
    def getHeight(self) -> int: ...
    @staticmethod
    def getMatcher(*args, **kwargs) -> typing.Any: ...
    @staticmethod
    def getReadThreadResult(*args, **kwargs) -> typing.Any: ...
    def getWidth(self) -> int: ...
    def isCapturing(self) -> bool: ...
    def isConnected(self) -> bool: ...
    def isReadThreadRunning(self) -> bool: ...
    def isValidCalibration(self) -> bool: ...
    @staticmethod
    def read(*args, **kwargs) -> typing.Any: ...
    def setDownsampleFactor(self, arg0: float) -> None: ...
    def setTestImagePaths(self, arg0: str, arg1: str) -> None: ...
    def startCapture(self) -> bool: ...
    def startReadThread(self, timeout: int = 1000, rectify: bool = True) -> None: ...
    def stopCapture(self) -> None: ...
    pass
def bgr2bgra(arg0: numpy.ndarray) -> numpy.ndarray:
    pass
def bgr2rgba(arg0: numpy.ndarray) -> numpy.ndarray:
    pass
def bgra2rgba(arg0: numpy.ndarray) -> numpy.ndarray:
    pass
def cvMatIsEqual(arg0: numpy.ndarray, arg1: numpy.ndarray) -> bool:
    pass
def depth2xyz(arg0: numpy.ndarray, arg1: float) -> numpy.ndarray:
    pass
def disparity2depth(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray:
    pass
def disparity2xyz(arg0: numpy.ndarray, arg1: numpy.ndarray) -> numpy.ndarray:
    pass
def flip(arg0: numpy.ndarray, arg1: int) -> numpy.ndarray:
    pass
def getVersionMajor() -> int:
    pass
def getVersionMinor() -> int:
    pass
def getVersionPatch() -> int:
    pass
def getVersionString() -> str:
    pass
def normaliseDisparity(arg0: numpy.ndarray) -> numpy.ndarray:
    pass
def processStereo(*args, **kwargs) -> typing.Any:
    pass
def processStereoFiles(*args, **kwargs) -> typing.Any:
    pass
def readImage(arg0: str) -> numpy.ndarray:
    pass
def savePLY(arg0: str, arg1: numpy.ndarray, arg2: numpy.ndarray) -> bool:
    pass
def scaleImage(arg0: numpy.ndarray, arg1: float) -> numpy.ndarray:
    pass
def showImage(arg0: str, arg1: numpy.ndarray) -> int:
    pass
def xyz2depth(arg0: numpy.ndarray) -> numpy.ndarray:
    pass
