import unittest
from unittest.mock import patch
from src.db.tui import main_menu


class TestTUI(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input")
    def test_full_coverage(self, mock_input, mock_print):
        # Этот список имитирует ПОЛНЫЙ цикл работы со всеми ветками if/elif/else
        mock_input.side_effect = [
            "1",
            "1",
            "Ivan",
            "Ivanov",
            "20",
            "M",
            "1",
            "invalid",
            "2",
            "3",
            "1",
            "Petr",
            "Petrov",
            "21",
            "M",
            "3",
            "invalid",
            "4",
            "1",
            "4",
            "invalid",
            "999",
            "0",
        ]

        main_menu()

        # Проверяем, что выход сработал
        mock_print.assert_any_call("До свидания!")


if __name__ == "__main__":
    unittest.main()
