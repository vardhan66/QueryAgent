from mis.utils.custom_csv_reader import CustomCSVReader
from typing import List
from pathlib import Path
from llama_index.core.schema import Document
from pprint import pprint

parser = CustomCSVReader()
file_path = Path("./db_data/mis/student_data.csv")

data: List[Document] = parser.load_data(
    file=file_path
)

pprint(data)
