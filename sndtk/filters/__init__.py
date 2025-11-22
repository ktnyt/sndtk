from sndtk.filters.config import ConfigFilter
from sndtk.filters.gitignore import GitignoreFilter
from sndtk.filters.pattern import PatternFilter
from sndtk.filters.types import CompositeFileFilter

DEFAULT_FILTER = CompositeFileFilter(
    GitignoreFilter(),
    PatternFilter(),
    ConfigFilter(),
)
