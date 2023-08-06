import json
import os
import pytest
from docparser.doc_parser_factory import DocParserFactory
from tests.excel_config import ExcelConfig as Config

doc1_config = {}
test_config = {
    "id": "cma",
    "name": "cma_config",
    "kv": {
        "VESSEL": {
            "position_pattern": [r"^VESSEL:"],
            "value_pattern": [
                r"(?P<Vessel>[\w\W]*?)(?:\r\n|\n|$)"],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [""],
            "action": [
                {"keyword": "VesselName", "key": "Vessel"},
            ]
        },
        "VOYAGE": {
            "position_pattern": [r"^VOYAGE:"],
            "value_pattern": [
                r"VOYAGE\s*:\s*(?P<VOYAGE>[\w\W]*)"],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [""],
            "action": [
                {"keyword": "VoyageNo", "key": "VOYAGE"},
            ]
        },
        "POD ETA": {
            "position_pattern": [r"^POD ETA"],
            "value_pattern": [r"POD\s*ETA\s*:\s*(?P<ETA>\d+/\d+/\d+)(?:\r\n|\n)"],
            "repeat_count": 1,
            "find_mode": "default",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [""],
            "action": [
                {"keyword": "EstimatedArrivalDate", "key": "ETA"}
            ]
        },
        "DeliveryPlaceName": {
            "position_pattern": [r"^OPERATIONAL LOAD PORT"],
            "value_pattern": [r"[\w\W]*?(?:\n|\r\n|)(?P<DELIVERY>.*)"],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [""],
            "action": [
                {"keyword": "DeliveryPlaceName", "key": "DELIVERY"}
            ]
        },
        "BillOfLadingsId": {
            "position_pattern": [r"^POD ETA"],
            "value_pattern": [r"[\w\W]*?(?P<billoflading>[a-zA-Z]{4}\s*[a-zA-Z]{3,}\d{7,})\s*Waybill"],
            "repeat_count": 1,
            "find_mode": "h",
            "separator_mode": "regex",
            "is_split_cell": 0,
            "split_pattern": [""],
            "action": [
                {"keyword": "BillOfLadingsId", "key": "billoflading"}
            ]
        }
    },
    "table": {
        "containers": {
            "position_pattern": [r"^CONTAINER\s*#"],
            "separator": " ",
            "find_mode": "v",
            "separator_mode": "regex",
            "column": ["ContainerNo"],
            "behaviors": [
                {
                    "over_action": "row",
                    "value_pattern": [r"(?P<col_1>([a-zA-Z]{4,}\d{7,}\s*)*)"],
                    "action": []
                }
            ]
        }
    },
    "data_type_format": {
        "VoyageNo": {"data_type": "str", "filter": "r([/\s])"},
        "EstimatedArrivalDate": {"data_type": "time", "format": "%m/%d/%Y", "filter": ""},
        "BillOfLadingsId": {"data_type": "str", "filter": "(\\s)"}
    },
    "address_repair": {
        "db": {
            "pub": {"user": "co", "pwd": "Co&23@2332$22", "server": "db.dev.com:1433",
                    "database": "CO_PUB"}
        },
        "repairs": [

            {"key": "DeliveryPlaceName", "db_key": "pub",
             "sql": "SELECT  [FullName],[LocalName],[name],[code],[Id] from Places WHERE IsDeleted = 0 and IsOcean = 1 and IsValid = 1 and ([FullName] like '%${value}%' or charindex([FullName],'${value}')> 0) ;",
             "column": [0, 1, 2, 3], "value": 4, "mapping": "DeliveryPlaceId",
             "old_val_handle": "empty"}
        ]
    }
}


class TestExcelDocumentParser:

    def test_excel_file_parse(self):
        """
        单文件测试
        :return:
        """
        name = "cma".upper()

        doc1_config["id"] = f"AN_{name}_"

        test_config["id"] = name
        test_config["name"] = f"{name} config"
        doc1_config["parse"] = test_config
        # print(test_config)
        print(json.dumps(test_config))
        factory = DocParserFactory.create("excel2",
                                          r"C:\Users\APing\Documents\WXWork\1688855080303598\Cache\File\2022-04\SMLINE.xlsx",
                                          test_config)
        result, errors = factory.parse()

        print(result, errors)


    # def test_excel_dir_parse(self):
    #     """
    #     测试文件夹下的拥有对应名称配置的excel文件
    #     :return:
    #     """
    #     path = os.getcwd() + "\\files"
    #     dirs = os.listdir(path)
    #     for file in dirs:
    #         name = file.split(".")[0]
    #         if ".xlsx" in file:
    #             _config = Config.get_config(name.lower())
    #             if _config is None:
    #                 continue
    #             factory = DocParserFactory.create("excel2", "%s\\%s.xlsx" % (path, name.lower()), _config)
    #             result, errors = factory.parse()
    #             print("=========================", file, "========================")
    #             print(_config)
    #             print(path + file)
    #             print(result)
    #             print(errors)
    #             print("------------------------------------------------------------")
    #             print("\r\n\r\n")


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
