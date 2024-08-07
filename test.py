from mis.utils.custom_csv_reader import CustomCSVReader
from llama_index.core import SimpleDirectoryReader
from pathlib import Path
from pprint import pprint 

try:
    csv_prefixes = [
            ("My name is ", ". I am a student at Vasireddy Venkatadri Institute of Technology.\n"),
            ("My roll no is ", ". \n"),
            ("My nptel status is ", ".\n"),
            ("My mobile no is ", ".\n"),
            ("I am pursuing B.tech in branch ", ".\n"),
            ("I am in section ", ".\n")
    ]

    parser = CustomCSVReader()
    file_path = Path("./db_data/mis/student_data.csv")

    documents = parser.load_data(file=file_path, csv_prefixes=csv_prefixes)
    pprint(documents)

except ImportError:
    raise ImportError("Module csv not found")

