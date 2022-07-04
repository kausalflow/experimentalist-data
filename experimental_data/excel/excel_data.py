from pathlib import Path
from typing import List, Dict
import pandas as pd
from multiprocessing import Pool
from loguru import logger


class ExcelData:
    def __init__(
        self, path: Path, processes: int = 1, read_excel_kwargs: Dict = {}
    ):
        self.path = path
        self.processes = processes
        self.read_excel_kwargs = read_excel_kwargs

    @property
    def files(self) -> List[Dict]:
        xlsx_paths = self.path.glob("**/*.xlsx")
        return [
            {
                "name": p.stem,
                "path": p,
                "folder": str(p.parent),
            }
            for p in xlsx_paths
        ]

    def _file_to_dataframe(self, file: Dict) -> Dict:
        logger.info(f"Reading {file['name']}")
        df = pd.read_excel(file["path"], **self.read_excel_kwargs)
        df["extras_folder"] = file["folder"]
        df["extras_name"] = file["name"]
        df["extras_path"] = file["path"]

        return df

    def _all_files_to_dataframe(self) -> pd.DataFrame:
        pool = Pool(processes=self.processes)
        df_list = pool.map(self._file_to_dataframe, self.files)

        df = pd.concat(df_list)

        return df

    def __call__(self) -> pd.DataFrame:
        df = self._all_files_to_dataframe()
        return df
