from typing import Any
from collections import defaultdict

obj_registry: defaultdict[Any, dict[str, Any]] = defaultdict(dict)
