from DotDict import DotDict


class Trigger():
    def __init__(self, trigger_info: DotDict):
        self.area = trigger_info.area
        self.color = trigger_info.color

    def __repr__(self) -> str:
        return f'{self.__dict__}'
