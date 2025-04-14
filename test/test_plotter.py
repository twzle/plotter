import unittest
from unittest.mock import patch, MagicMock, call
import os
import matplotlib.pyplot as plt
from src.stats import Stats
from src.plotter import Plotter, log_draw  # Импортируем декоратор отдельно

class TestPlotter(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_stats = Stats(
            scheduler_total_time=100.0,
            scheduler_processing_time=80.0,
            scheduler_idle_time=15.0,
            scheduler_wait_time=5.0,
            scheduler_packet_processing_delay=0.005,
            queue_packet_processing_delays={1: 0.002, 2: 0.003},
            user_packet_processing_delays={101: 0.001, 102: 0.004},
            scheduler_throughput=50.5,
            max_scheduler_throughput=100.0,
            scheduler_unused_resources=0.3
        )
        
        # Создаем директорию для выходных файлов, если ее нет
        os.makedirs("output", exist_ok=True)

    def tearDown(self):
        """Очистка после тестов"""
        # Удаляем созданные файлы
        for f in os.listdir("output"):
            os.remove(os.path.join("output", f))
        os.rmdir("output")

    @patch("matplotlib.pyplot.bar")
    @patch("matplotlib.pyplot.tight_layout")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.xlabel")
    @patch("matplotlib.pyplot.ylabel")
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.close")
    def test_draw_queue_packet_processing_delay_pie_chart(
        self, mock_close, mock_savefig, mock_ylabel, 
        mock_xlabel, mock_title, mock_tight, mock_bar):
        """Тест генерации графика задержек в очередях"""
        plotter = Plotter(self.test_stats)
        
        # Меняем декоратор на обычную функцию для теста
        original_method = plotter.draw_queue_packet_processing_delay_pie_chart.__wrapped__
        result = original_method(
            plotter,
            self.test_stats.scheduler_packet_processing_delay,
            self.test_stats.queue_packet_processing_delays
        )
        
        # Проверяем вызовы matplotlib
        mock_bar.assert_called_once()
        mock_title.assert_called_once_with("Задержка обслуживания пакетов в очередях", pad=20)
        mock_xlabel.assert_called_once_with("Номер очереди")
        mock_ylabel.assert_called_once_with("Задержка (мс)")
        mock_tight.assert_called_once()
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
        
        # Проверяем путь сохранения
        self.assertTrue(result.endswith("output/queue_packet_processing_delay_bar_chart.png"))

    @patch("matplotlib.pyplot.pie")
    @patch("matplotlib.pyplot.axis")
    @patch("matplotlib.pyplot.title")
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.close")
    def test_draw_modelling_time_pie_chart(
        self, mock_close, mock_savefig, mock_title, 
        mock_axis, mock_pie):
        """Тест генерации круговой диаграммы времени моделирования"""
        plotter = Plotter(self.test_stats)
        
        # Меняем декоратор на обычную функцию для теста
        original_method = plotter.draw_modelling_time_pie_chart.__wrapped__
        result = original_method(
            plotter,
            self.test_stats.scheduler_processing_time,
            self.test_stats.scheduler_idle_time,
            self.test_stats.scheduler_wait_time
        )
        
        # Проверяем параметры pie
        mock_pie.assert_called_once()
        args, kwargs = mock_pie.call_args
        self.assertEqual(kwargs['autopct'], '%1.1f%%')
        self.assertEqual(kwargs['startangle'], 140)
        
        mock_axis.assert_called_once_with('equal')
        mock_title.assert_called_once_with("Время моделирования", pad=20)
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()

    @patch("matplotlib.pyplot.bar")
    @patch("matplotlib.pyplot.legend")
    @patch("matplotlib.pyplot.savefig")
    @patch("matplotlib.pyplot.close")
    def test_draw_scheduler_throughput_bar_chart(
        self, mock_close, mock_savefig, mock_legend, mock_bar):
        """Тест генерации столбчатой диаграммы пропускной способности"""
        plotter = Plotter(self.test_stats)
        
        # Тестовые данные
        scheduler_throughput = 50.5
        max_scheduler_throughput = 100.0
        scheduler_unused_resources = 0.3
        max_scheduler_resources = 1.0
        
        # Вызываем метод
        result = plotter.draw_scheduler_throughput_bar_chart(
            scheduler_throughput,
            max_scheduler_throughput,
            scheduler_unused_resources,
            max_scheduler_resources
        )
        
        # Проверяем основные моменты:
        
        # 1. Проверяем вызовы bar()
        # Должно быть 4 вызова (2 группы по 2 столбца)
        self.assertEqual(mock_bar.call_count, 4)
        
        # 2. Проверяем легенду
        mock_legend.assert_called_once_with(
            framealpha=0.9,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0
        )
        
        # 3. Проверяем сохранение файла
        mock_savefig.assert_called_once()
        
        # 4. Проверяем что close вызывался (не проверяем точное количество)
        self.assertTrue(mock_close.call_count >= 1)
        
        # 5. Проверяем возвращаемый путь
        self.assertTrue(result.endswith("output/scheduler_throughput_bar_chart.png"))

    @patch.object(Plotter, 'draw_modelling_time_pie_chart')
    @patch.object(Plotter, 'draw_queue_packet_processing_delay_pie_chart')
    @patch.object(Plotter, 'draw_user_packet_processing_delay_bar_chart')
    @patch.object(Plotter, 'draw_scheduler_throughput_bar_chart')
    def test_run_success(
        self, mock_throughput, mock_user_delay, 
        mock_queue_delay, mock_time_pie):
        """Тест успешного выполнения метода run"""
        plotter = Plotter(self.test_stats)
        plotter.run()
        
        # Проверяем вызовы всех методов отрисовки
        mock_time_pie.assert_called_once()
        mock_queue_delay.assert_called_once()
        mock_user_delay.assert_called_once()
        mock_throughput.assert_called_once()

    @patch.object(Plotter, 'draw_modelling_time_pie_chart')
    @patch("builtins.print")
    def test_run_with_exception(self, mock_print, mock_pie):
        """Тест обработки исключений в методе run"""
        # Создаем тестовое исключение
        test_exception = Exception("Test error")
        mock_pie.side_effect = test_exception
        
        plotter = Plotter(self.test_stats)
        plotter.run()
        
        # Проверяем, что print был вызван с тем же сообщением исключения
        args, _ = mock_print.call_args
        self.assertEqual(str(args[0]), "Test error")

    @patch("builtins.print")
    def test_log_draw_decorator(self, mock_print):
        """Тест декоратора log_draw"""
        # Создаем тестовую функцию с декоратором
        @log_draw
        def test_func():
            return "./test/path.png"
            
        # Вызываем функцию
        test_func()
        
        # Проверяем вывод
        mock_print.assert_called_once_with(
            f"test_func: Done.\nSaved to {os.getcwd()}/test/path.png\n"
        )

if __name__ == '__main__':
    unittest.main()