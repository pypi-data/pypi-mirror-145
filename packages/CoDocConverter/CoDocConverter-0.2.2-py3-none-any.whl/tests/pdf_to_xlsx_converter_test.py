# Press the green button in the gutter to run the script.
import os
import pytest

from docconverter.doc_converter_factory import DocConverterFactory


class TestClass:
    def test_pdf_to_xlsx_convert(self):
        converter = DocConverterFactory.create('pdf', 'xlsx')
        output_file = converter.convert(os.getcwd() + "\\files\\CMA.pdf",
                                        os.getcwd().replace("\\tests","") +"\\output",
                                        timeout=10,
                                        exe=(os.getcwd() + "\\libs\\acrobat_pdf.exe").replace('\\tests', ''))

        assert output_file is not None

    def test_pdf_to_txt_bulk_convert(self):
        converter = DocConverterFactory.create('pdf', 'xlsx')
        output_files = converter.bulk_convert([os.getcwd() + "\\files\\CMA.pdf"],
                                              os.getcwd().replace("\\tests", "") + "\\output",
                                              timeout=10,
                                              exe=(os.getcwd() + "\\libs\\acrobat_pdf.exe").replace('\\tests','')
                                              )

        assert len(output_files) == 1


if __name__ == '__main__':
    pytest.main("-q --html=report.html")
