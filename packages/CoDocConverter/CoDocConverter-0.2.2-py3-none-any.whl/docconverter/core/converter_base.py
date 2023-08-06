# -*- coding: utf-8 -*-

class DocConverterBase:
    """
    文档转换抽象基类
    """

    def __init__(self):
        pass

    def convert(self, input_file, output_dir,**args):
        """
        文档转换
        :param input_file:转换文件路径
        :param output_dir: 输出目录
        :return: 无
        """
        pass

    def bulk_convert(self, input_files, output_dir,**args):
        """
        批量文档转换
        :param input_files:批量文件
        :param output_dir: 输出目录
        :return: 无
        """
        pass
