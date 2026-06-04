import unittest
from unittest.mock import patch
from src.db.tui import main_menu


class TestTUI(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input")
    def test_full_coverage(self, mock_input, mock_print):
        # Имитируем выбор In-Memory БД (1) и затем выход (0)
        mock_input.side_effect = ["1", "0"]
        main_menu()
        mock_print.assert_any_call("До свидания!")


if __name__ == "__main__":
    unittest.main()
