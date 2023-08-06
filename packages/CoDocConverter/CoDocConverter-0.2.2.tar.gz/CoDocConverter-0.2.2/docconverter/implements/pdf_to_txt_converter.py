import os

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

from docconverter.core.converter_base import DocConverterBase


class PdfToTxtConverter(DocConverterBase):
    """
    PDF转文本批量转换器
    """

    def __init__(self):
        self.debug = 0
        self.password = b''
        self.page_nos = set()
        self.max_pages = 0
        self.image_writer = None
        self.rotation = 0
        self.encoding = 'utf-8'
        self.scale = 1
        self.caching = True
        self.la_params = LAParams()

    def convert(self, input_file, output_dir, **args):
        """
        转换
        :param input_file: 输入文件
        :param output_dir: 输出文件
        :return:
        """

        if not input_file.lower().endswith(".pdf"):
            return

        PDFDocument.debug = self.debug
        PDFParser.debug = self.debug
        CMapDB.debug = self.debug
        PDFPageInterpreter.debug = self.debug

        rsrc_mgr = PDFResourceManager(caching=False)
        file_name = os.path.basename(input_file)
        base_name,_ = os.path.splitext(file_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        if "suffix" in args:
            output_file_path = '%s\\%s_%s.txt' % (output_dir, base_name, args["suffix"])
        else:
            output_file_path = '%s\\%s.txt' % (output_dir, base_name)

        out_file = open(output_file_path, 'w', encoding=self.encoding)
        device = TextConverter(rsrc_mgr, out_file, laparams=self.la_params,
                               imagewriter=self.image_writer)

        try:
            with open(input_file, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrc_mgr, device)
                for page in PDFPage.get_pages(fp, self.page_nos,
                                              maxpages=self.max_pages, password=self.password,
                                              caching=False, check_extractable=True):
                    page.rotate = (page.rotate + self.rotation) % 360
                    interpreter.process_page(page)

            return output_file_path
        except:
            raise ("文件%s转换失败!" % input_file)
        finally:
            device.close()
            out_file.close()

    def bulk_convert(self, input_files, output_dir, **args):
        """
        批量文档转换
        :param input_files:批量文件
        :param output_dir: 输出目录
        :return: 无
        """

        out_put_files = []
        for file in input_files:
            out_put_files.append(self.convert(file, output_dir, **args))

        return out_put_files
