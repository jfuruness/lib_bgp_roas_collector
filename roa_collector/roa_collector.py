import csv
from ipaddress import ip_network
import re
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any, Optional

from requests_cache import CachedSession
from roa_checker import ROA


class ROACollector:
    """This class downloads, and stores ROAs from rpki validator"""

    URL: str = "https://rpki-validator.ripe.net/api/export.json"

    def __init__(
        self,
        csv_path: Optional[Path] = None,
        requests_cache_db_path: Optional[Path] = None,
    ):
        self.csv_path: Optional[Path] = csv_path
        if requests_cache_db_path is None:
            requests_cache_db_path = Path(f"/tmp/{date.today()}.db")
        self.requests_cache_db_path: Path = requests_cache_db_path
        self.session: CachedSession = CachedSession(str(self.requests_cache_db_path))

    def __del__(self):
        self.session.close()

    def run(self) -> tuple[ROA, ...]:
        """Downloads and stores roas from a json"""

        roas = self._parse_roa_json(self._get_json_roas())
        self._write_csv(roas)
        return roas

    def _get_json_roas(self) -> list[dict[Any, Any]]:
        """Returns the json from the url for the roas"""

        headers = {"Accept": "application/xml;q=0.9,*/*;q=0.8"}
        response = self.session.get(self.URL, headers=headers)
        response.raise_for_status()
        roas_list = response.json()["roas"]
        assert isinstance(roas_list, list), "(for mypy) not a list? {roas_list}"
        return roas_list

    def _parse_roa_json(
        self, unformatted_roas: list[dict[Any, Any]]
    ) -> tuple[ROA, ...]:
        """Parse JSON into a tuple of ROA objects"""

        formatted_roas = []
        for roa in unformatted_roas:
            formatted_roas.append(
                ROA(
                    prefix=ip_network(roa["prefix"]),
                    origin=int(re.findall(r"\d+", roa["asn"])[0]),
                    max_length=int(roa["maxLength"]),
                    # RIPE, afrinic, etc
                    ta=roa["ta"],
                )
            )
        return tuple(formatted_roas)

    def _write_csv(self, roas: tuple[ROA, ...]) -> None:
        """Writes ROAs to a CSV if csv_path is not None"""

        rows = list()
        for roa in roas:
            row_dict = asdict(roa)
            row_dict["prefix"] = str(row_dict["prefix"])
            rows.append(row_dict)

        if self.csv_path:
            with self.csv_path.open("w") as temp_csv:
                writer = csv.DictWriter(temp_csv, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows([x for x in rows])
