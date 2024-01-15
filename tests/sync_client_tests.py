import unittest
from xml.etree import ElementTree

from packaide_client.sync import PackaideClient

URL = "http://127.0.0.1:8000"


class TestSyncClient(unittest.TestCase):
    def setUp(self):
        self.client = PackaideClient(URL)

    def test_basic_operation(self):
        """ Test that two SVGs are combined into one sheet """
        total_number_of_shapes = 3

        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="100" />
        </svg>
        """

        outputs = self.client.pack([shape1, shape2], height=40, width=60)

        # Assert the correct number of output sheets
        self.assertEqual(1, len(outputs))

        # Assert the correct number of shapes
        output_as_xml = ElementTree.fromstring(outputs[0])

        self.assertEqual(total_number_of_shapes, len(output_as_xml))

    def test_multiple_sheets(self):
        """ Test that two SVGs are combined into one sheet """
        total_number_of_shapes = 4

        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="100" />
        <rect height="50" width="50" />
        </svg>
        """

        outputs = self.client.pack([shape1, shape2], height=2, width=2)

        self.assertEqual(3, len(outputs))

        # Assert the correct number of shapes
        shape_counter = 0
        for output in outputs:
            output_as_xml = ElementTree.fromstring(output)
            shape_counter += len(output_as_xml)

        self.assertEqual(total_number_of_shapes, shape_counter)

    def test_no_shapes_fit(self):
        """ Test when no given shapes fit onto the sheet """
        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="100" />
        </svg>
        """

        with self.assertRaises(ValueError):
            self.client.pack([shape1, shape2], height=1, width=1)

    def test_one_shape_too_large(self):
        """ Test when one shape is too large to fit onto a sheet """
        shape1 = """
        <svg>
        <rect height="100" width="100" />
        </svg>
        """

        shape2 = """
        <svg>
        <rect height="100" width="100" />
        <rect height="100" width="1000" />
        </svg>
        """

        with self.assertRaises(ValueError):
            self.client.pack([shape1, shape2], height=2, width=2)


if __name__ == '__main__':
    unittest.main()
