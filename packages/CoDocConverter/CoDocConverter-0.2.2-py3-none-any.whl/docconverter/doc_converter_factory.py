# -*- coding: utf-8 -*-
import importlib


class DocConverterFactory:
    """
    文档转换器创建工厂
    """

    @staticmethod
    def create(src_format, target_format):
        """
        根据类型创建对应类型的文档转换器
        """
        try:

            module_name = 'docconverter.implements.%s_to_%s_converter' % (src_format, target_format)

            class_name = '%sTo%sConverter' % (src_format.capitalize(), target_format.capitalize())
            converter_module = importlib.import_module(module_name)
            cls = getattr(converter_module, class_name)

            return cls()
        except ModuleNotFoundError:
            raise
