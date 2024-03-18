from pathlib import Path

from .roa_collector import ROACollector


def main():
    ROACollector(csv_path=Path.home() / "roas.csv").run()


if __name__ == "__main__":
    main()
