
# app/display_base.py
from abc import ABC, abstractmethod
from PIL import Image


class BaseDisplay(ABC):
    """所有電子紙實作都要遵守的介面"""

    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @abstractmethod
    def show_image(self, img: Image.Image) -> None:
        """顯示一張 PIL Image"""
        ...

    @abstractmethod
    def sleep(self) -> None:
        ...
