from typing import Optional

import numpy as np
from dataclasses import field, dataclass

@dataclass
class Record:
    text: str
    embedding: np.ndarray
    metadata: Optional[dict] = field(default_factory=dict)