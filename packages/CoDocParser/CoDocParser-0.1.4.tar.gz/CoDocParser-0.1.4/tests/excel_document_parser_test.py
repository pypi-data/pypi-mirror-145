import os
import pytest
from docparser.doc_parser_factory import DocParserFactory
from tests.excel_config import ExcelConfig as Config

class TestExcelDocumentParser:

    # def test_excel_file_parse(self):
    #     """
    #     单文件测试
    #     :return:
    #     """
    #     factory = DocParserFactory.create("excel", Config.excel_dir % "cma", Config.cma_config)
    #     result, errors = factory.parse()
    #     print(result, errors)
    #     assert len(errors) == 0

    def test_excel_dir_parse(self):
        """
        测试文件夹下的拥有对应名称配置的excel文件
        :return:
        """
        path = os.getcwd() + "\\files"
        dirs = os.listdir(path)
        for file in dirs:
            name = file.split(".")[0]
            if ".xlsx" in file:
                _config = Config.get_config(name.lower())
                if _config is None:
                    continue
                factory = DocParserFactory.create("excel2", "%s\\%s.xlsx" % (path, name.lower()), _config)
                result, errors = factory.parse()
                print("=========================", file, "========================")
                print(_config)
                print(path + file)
                print(result)
                print(errors)
                print("------------------------------------------------------------")
                print("\r\n\r\n")



if __name__ == '__main__':
    pytest.main("-q --html=report.html")
