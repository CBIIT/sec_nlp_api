
from dataclasses import dataclass


@dataclass
class Criteria:
    inclusions: [str]
    exclusions: [str]