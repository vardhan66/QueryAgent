from llama_index.core.readers.base import BaseReader
from typing import Any, Dict, List, Optional, Union, Tuple
from llama_index.core.schema import Document
from pathlib import Path


class CustomCSVReader(BaseReader):
    def __init__(self, *args: Any, concat_rows: bool = False, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.concat_rows = concat_rows

    def load_data(self, file: Path, csv_prefixes: Optional[List[Tuple[str]]] = None, extra_info: Optional[Dict] = None) -> \
            List[Document]:
        """Method for loading vectors"""

        try:
            import csv
        except ImportError:
            raise ImportError("csv module is required to load csv files")

        text_chunks = []
        with open(file) as fp:
            csv_data = csv.reader(fp)
            if csv_prefixes is not None:
                for row_idx, row in enumerate(csv_data):
                    # Adding prefix and suffix for each column in a record.
                    prefix_row = [csv_prefixes[col_idx][0] + col + csv_prefixes[col_idx][1] for col_idx, col in enumerate(row)]
                         
                    text_chunks.append(" ".join(prefix_row))
            else:
                for row in csv_data:
                    text_chunks.append(", ".join(row))

            meta_data = {"file_name": file.name, "extension": file.suffix}

            if extra_info:
                meta_data = {**meta_data, **extra_info}

            if self.concat_rows:
                return [Document(text="\n".join(text_chunks), meta_data=meta_data)]
            else:
                return [Document(text=text, meta_data=meta_data) for text in text_chunks]
