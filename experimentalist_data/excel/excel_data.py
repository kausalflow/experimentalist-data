from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd
from loguru import logger


class ExcelData:
    """
    Parse excel files in multiple files into a single dataframe.

    ```python
    ed = ExcelData(
        path=".", read_excel_kwargs={"sheet_name": "Sheet1", usecols="A:B"}
    )
    ```

    :param path: Path to the folder containing the excel files.
    :param processes: Number of processes to use.
    :param read_excel_kwargs: Keyword arguments to pass to pandas.read_excel.
    :param file_extension: File extension to look for.
    """
    def __init__(
        self, path: Union[Path, str],
        processes: int = 1, read_excel_kwargs: Dict = {},
        file_extension: str = "xlsx",
    ):
        if isinstance(path, str):
            self.path = Path(path)
        elif isinstance(path, Path):
            self.path = path
        else:
            raise TypeError(f"path must be a string or Path, not {type(path)}")
        self.processes = processes
        self.read_excel_kwargs = read_excel_kwargs
        self.file_extension = file_extension

    @property
    def files(self) -> List[Dict]:
        xlsx_paths = self.path.glob(f"**/*.{self.file_extension}")
        return [
            {
                "name": p.stem,
                "path": p,
                "folder": str(p.parent),
            }
            for p in xlsx_paths
            if not p.stem.startswith("~$")
        ]

    def _file_to_dataframe(self, file: Dict) -> Dict:
        logger.info(f"Reading {file['name']}")
        df = pd.read_excel(file["path"], **self.read_excel_kwargs)
        df["extras_folder"] = file["folder"]
        df["extras_name"] = file["name"]
        df["extras_path"] = file["path"]

        return df

    def _all_files_to_dataframe(self) -> pd.DataFrame:
        if self.processes >= 1:
            pool = Pool(processes=self.processes)
            df_list = pool.map(self._file_to_dataframe, self.files)
        else:
            df_list = [self._file_to_dataframe(f) for f in self.files]

        df = pd.concat(df_list)

        return df

    def __call__(self) -> pd.DataFrame:
        df = self._all_files_to_dataframe()
        return df
