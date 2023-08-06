import json
import unittest
from os.path import dirname, join

from dotenv import load_dotenv

from pdf_generator.generator import PDFGenerator

load_dotenv()


class PDFGeneratorTestCase(unittest.TestCase):

    @staticmethod
    def test_manual_json():
        file_name = 'test_jsons/input_bak_2131.json'
        kwargs = {
            "doctor_notes": json.loads(open(join(dirname(__file__), file_name)).read())
        }

        pdf_generator = PDFGenerator(**kwargs)
        pdf_buffer = pdf_generator.get_buffer()
        pdf_buffer_discharge = pdf_generator.get_buffer_discharge()

        output_file = file_name.replace('.json', '.pdf').replace('input', 'output')
        try:
            with open(output_file, 'wb') as file:
                file.write(pdf_buffer.getbuffer())
        except FileNotFoundError:
            pass

        try:
            with open(output_file.replace('output', 'discharge_output'), 'wb') as file:
                file.write(pdf_buffer_discharge.getbuffer())
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
