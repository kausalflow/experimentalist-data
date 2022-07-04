from experimental_data.excel.excel_data import ExcelData

def test_excel_data(base_data):

    ed = ExcelData(base_data)

    ed()


def test_excel_data_multiprocessing(base_data):

    ed = ExcelData(base_data, processes=3)

    ed()
