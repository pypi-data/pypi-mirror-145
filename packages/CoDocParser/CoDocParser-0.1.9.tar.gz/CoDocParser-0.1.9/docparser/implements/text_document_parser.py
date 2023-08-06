import re
import os

from fileio import File

from docparser.core.document_parser_base import DocumentParserBase


class TextDocumentParser(DocumentParserBase):
    """
    文本文件解析器
    """

    def __init__(self, file, configs):
        """
        初始化
        :param file:文件路径
        :param configs: 配置
        """
        self._file = file
        self._configs = configs

        if not os.path.exists(file):
            raise FileNotFoundError

        self._data = File.textread(file)

    def parse(self):
        """
        根据配置抽取数据
        :return: 返回抽取的数据
        """

        data_bucket = {}
        for key in self._configs.keys():
            item_config = self._configs[key]
            match_group = re.search(
                r"%s" % item_config['pattern'], self._data, re.M)
            match_text = '' if match_group is None else match_group.group(
                key)

            data_bucket[key] = match_text

        return data_bucket


if __name__ == '__main__':
    converter = TextDocumentParser(
        r"C:\Users\86134\Desktop\projects\email\653\cmacgm_noticeofarrival_csclyellowsea_0bh9ew1ma-at210727102222_769469_000019.xlsx",
        {
            # "vessel_name": {
            #     "type": "text",
            #     "rect": {
            #         "left_keyword": "VESSEL:",
            #         "right_keyword": "VOYAGE:",
            #         "bottom_keyword": "OPERATIONAL DISCH. PORT: PLACE"
            #     },
            #     "pattern": ".*"
            # },
            # "pod_eta": {
            #     "type": "text",
            #     "rect": {
            #         "left_keyword": "POD ETA:",
            #         "bottom_keyword": "FPD ETA:"
            #     },
            #     "pattern": ".*"
            # },
            # "it_number:": {
            #     "type": "text",
            #     "rect": {
            #         "left_keyword": "IT NUMBER:",
            #         "right_keyword": "PLACE OF ISSUE:",
            #     },
            #     "pattern": ".*"
            # },
            # "it_issued_date:": {
            #     "type": "text",
            #     "rect": {
            #         "left_keyword": "IT ISSUED DATE:",
            #     },
            #     "pattern": ".*"
            # },
            # "firms_code": {
            #     "type": "text",
            #     "rect": {
            #         "left_keyword": "FIRMS CODE:",
            #     },
            #     "pattern": ".*"
            # },
            # "shipper": {
            #     "type": "text",
            #     "rect": {
            #         "top_keyword": "SHIPPER",
            #         "bottom_keyword": "PLEASE NOTE :",
            #     },
            #     "pattern": ".*"
            # }

            "containers": {
                "type": "table",
                "extractor": "mixed",
                "max_rows": 1,
                "row_split_ref_col_name": "container_no",
                "col_split_chars": "  ",
                "rect": {
                    "top": {
                        "keyword": "CONTAINER  # ",
                        "include": True
                    },
                    "bottom": {
                        "keyword": "PLEASE NOTE :",
                    }
                },
                "columns": [
                    {
                        "name": "container_no",
                        "title": "CONTAINER #",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "content_pattern": "\\w{0,20}",
                    }, {
                        "name": "seal_no",
                        "title": "SEAL #",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "content_pattern": "\\w{0,20}",
                    }, {
                        "name": "container_size_type",
                        "title": "SIZE/TYPE #",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "content_pattern": "\\d{1,10}\\s{1,2}\\[a-z|A-Z]{2,5}",
                    }, {
                        "name": "weight",
                        "title": "WEIGHT",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "content_pattern": "\\d{0,10}",
                    }, {
                        "name": "measure",
                        "title": "MEASURE",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "content_pattern": "\\w{0,5}",
                    }, {
                        "name": "free_business_last_free",
                        "title": "FREE BUSINESS LAST FREE",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "childrens": [
                            {
                                "name": "day_at_port",
                                "title": "DAYS AT PORT",
                                "title_h_align": "center",
                                "title_v_align": "middle",
                                "content_pattern": "\\w{0,20}",
                            },
                            {
                                "name": "day_at_ramp",
                                "title": "DAY AT RAMP",
                                "title_h_align": "center",
                                "title_v_align": "middle",
                                "content_pattern": "\\d{1,2}/\\d{1,2}/\\d{1,2}",
                            }
                        ]
                    }, {
                        "name": "pickup_no",
                        "title": "PICKUP #",
                        "title_h_align": "center",
                        "title_v_align": "middle",
                        "content_pattern": "\\w{0,20}",
                    },
                ]
            }
        })
    data = converter.extract()
    print(data)
