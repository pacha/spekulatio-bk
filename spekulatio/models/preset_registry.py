
from spekulatio import Model

from . import Preset


class PresetRegistry(Model):
    presets: list[Preset] = []
    _index: dict[str, Preset] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize index
        for preset in self.presets:
            self._index[preset.name] = preset

    def __getitem__(self, name: str) -> Preset:
        return self._index[name]

