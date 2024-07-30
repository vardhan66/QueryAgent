from llama_index.core.readers.base import BaseReader
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class CustomCSVReader(BaseReader):
    def __init__(self, *args: Any, concat_rows: bool = False, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.concat_rows = concat_rows

    def load_data(self, file: Path, csv_prefixes: Optional[List[str]] = None, extra_info: Optional[Dict] = None) -> \
            Union[List[str], List[List[str]]]:
        """Method for loading vectors"""

        try:
            import csv
        except ImportError:
            raise ImportError("csv module is required to load csv files")

        text_chunks = []
        with open(file) as fp:
            csv_data = csv.reader(fp)

            if csv_prefixes is not None:
                for idx, column in enumerate(csv_data):
                    csv_data[idx] = csv_prefixes[idx] + column
            else:
                for row in csv_data:
                    text_chunks.append(", ".join(row))

        return text_chunks
