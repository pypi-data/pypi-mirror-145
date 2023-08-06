# Press the green button in the gutter to run the script.
import os
import pytest

from docconverter.doc_converter_factory import DocConverterFactory


class TestPdfToTxtConverter:
    def test_pdf_to_txt_convert(self):
        converter = DocConverterFactory.create('pdf', 'txt')
        output_file = converter.convert(os.getcwd() + "\\files\\主提单.pdf",os.getcwd().replace("\\tests","") +"\\output")

        assert output_file is not None

    def test_pdf_to_txt_bulk_convert(self):
        converter = DocConverterFactory.create('pdf', 'txt')
        output_files = converter.bulk_convert([os.getcwd() + "\\files\\zim.pdf"], os.getcwd().replace("\\tests","") +r"\output")

        assert len(output_files) == 1


if __name__ == '__main__':
    pytest.main()
