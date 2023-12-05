from dataclasses import dataclass


@dataclass(frozen=True)
class ROA:
    asn: int
    prefix: str
    max_length: int
    # RIPE, afrinic, etc (ta comes from the JSON)
    ta: str

    @property
    def origin(self) -> int:
        """Useful when calling this from other libraries that expect origin"""
        return self.asn
