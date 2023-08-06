# -*- coding: utf-8 -*-
import importlib
import os

from docparser.core import easy_cache

easy_cache._init()


class DocParserFactory:
    """
    文档解析器创建工厂
    """

    @staticmethod
    def create(doc_type, file, config):
        """
        根据类型创建对应类型的文档解析器

        """
        try:

            module_name = 'docparser.implements.%s_document_parser' % doc_type

            class_name = '%sDocumentParser' % doc_type.capitalize()
            virtual_block_module = importlib.import_module(module_name)
            cls = getattr(virtual_block_module, class_name)

            return cls(file, config)
        except ModuleNotFoundError:
            raise


# if __name__ == "__main__":
#
#     smline_config = {'id': 'SMLINE', 'name': 'SMLINE config', 'kv': {'Arrival Vessel': {'position_pattern': ['^Arrival Vessel'], 'value_pattern': ['Arrival Vessel\\s*:\\s*(\\w*\\s*\\w*\\s*\\d+\\s+\\w+)\\s{4,}[\\w\\W]*?\\nB/L No\\s*:\\s*([\\w]*?)\\s{1,}'], 'repeat_count': 1, 'find_mode': 'default', 'separator_mode': 'regex', 'is_split_cell': 0, 'split_pattern': [''], 'action': [{'keyword': 'Arrival Vessel'}, {'keyword': 'BillOfLadingsId'}]}, 'ETA': {'position_pattern': ['^ETA/ETB'], 'value_pattern': ['[\\w\\W]*?(\\d{2,}\\s*[a-zA-Z]{3,}\\s*\\d{2,}\\s*\\d{2,}\\:\\d{2,}\\([a-zA-Z]{2}\\))[\\w\\W]*?(\\d{2,}\\s*[a-zA-Z]{3,}\\s*\\d{2,}\\s*\\d{2,}\\:\\d{2,})[\\w\\W]*?([a-zA-Z]{3,}\\s*\\d+\\s*[a-zA-Z]{3,})'], 'repeat_count': 1, 'find_mode': 'h', 'separator_mode': 'regex', 'is_split_cell': 0, 'split_pattern': [''], 'action': [{'keyword': 'ETA'}, {'keyword': 'vailable Date'}, {'keyword': 'Port Free Time'}]}}, 'table': {'bill': {'position_pattern': ['^CONTAINER#'], 'separator': '\n', 'find_mode': 'h', 'separator_mode': 'regex', 'column': ['CHG', 'RATED AS', 'RATE', 'PE', 'COLLECT'], 'behaviors': [{'over_action': 'row', 'loop': 1, 'value_pattern': ['(?P<col_1>[a-zA-Z]*\\s{1,}[a-zA-Z]*)\\s{1,}(?P<col_2>\\d{1,}\\.\\d{1,})\\s{1,}(?P<col_3>\\d{1,}\\.\\d{1,})\\s*(?P<col_4>\\w{1,})\\s{1,}(?P<col_5>\\d{1,}\\.\\d{1,})(?:\\n|$)'], 'action': []}, {'over_action': 'end', 'value_pattern': ['^(DESTINATION)']}]}}, 'data_type_format': {'ETA': {'data_type': 'time', 'format': '%d %b %y %H:%M', 'filter': '(\\(CY\\))'}, 'vailable Date': {'data_type': 'time', 'format': '%d %b %y %H:%M', 'filter': '(\\n)'}}}
#
#     factory = DocParserFactory.create("excel2", "F:\\workspace\\python\\cityocean\\cots.libs\\cots.libs.docparser\\tests\\files\\smline.xlsx", smline_config)
#     result, errors = factory.parse()
#     print(result, errors)