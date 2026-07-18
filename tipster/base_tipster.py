from abc import ABC, abstractmethod

class BaseTipster(ABC):

    @abstractmethod
    def get_predictions(self, date_str: str):
        pass
