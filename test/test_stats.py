import unittest
import tempfile
import os
from src.stats import Stats, load_stats_from_yaml, yaml

class TestStats(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_data = {
            "scheduler_total_time": 100.0,
            "scheduler_processing_time": 80.0,
            "scheduler_idle_time": 15.0,
            "scheduler_wait_time": 5.0,
            "scheduler_packet_processing_delay": 0.005,
            "queue_packet_processing_delays": {1: 0.002, 2: 0.003},
            "user_packet_processing_delays": {101: 0.001, 102: 0.004},
            "scheduler_throughput": 50.5,
            "max_scheduler_throughput": 100.0,
            "scheduler_unused_resources": 0.3
        }
        
        # Создаем временный YAML файл
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml')
        with open(self.temp_file.name, 'w') as f:
            yaml.dump(self.test_data, f)
    
    def tearDown(self):
        """Удаление временного файла"""
        os.unlink(self.temp_file.name)

    def test_stats_initialization(self):
        """Тест инициализации Stats с полным набором параметров"""
        stats = Stats(**self.test_data)
        
        self.assertEqual(stats.scheduler_total_time, 100.0)
        self.assertEqual(stats.scheduler_processing_time, 80.0)
        self.assertEqual(stats.scheduler_idle_time, 15.0)
        self.assertEqual(stats.scheduler_wait_time, 5.0)
        self.assertEqual(stats.scheduler_packet_processing_delay, 0.005)
        self.assertDictEqual(stats.queue_packet_processing_delays, {1: 0.002, 2: 0.003})
        self.assertDictEqual(stats.user_packet_processing_delays, {101: 0.001, 102: 0.004})
        self.assertEqual(stats.scheduler_throughput, 50.5)
        self.assertEqual(stats.max_scheduler_throughput, 100.0)
        self.assertEqual(stats.scheduler_unused_resources, 0.3)

    def test_stats_default_values(self):
        """Тест инициализации Stats с пропущенными параметрами"""
        stats = Stats(
            scheduler_total_time=100.0,
            scheduler_processing_time=80.0,
            scheduler_idle_time=15.0,
            scheduler_wait_time=5.0,
            scheduler_packet_processing_delay=0.005,
            queue_packet_processing_delays={},
            user_packet_processing_delays={},
            scheduler_throughput=0.0,
            max_scheduler_throughput=0.0,
            scheduler_unused_resources=0.0
        )
        
        self.assertEqual(stats.scheduler_throughput, 0.0)
        self.assertEqual(stats.max_scheduler_throughput, 0.0)
        self.assertEqual(stats.scheduler_unused_resources, 0.0)
        self.assertDictEqual(stats.queue_packet_processing_delays, {})
        self.assertDictEqual(stats.user_packet_processing_delays, {})

    def test_str_representation(self):
        """Тест строкового представления объекта Stats"""
        stats = Stats(**self.test_data)
        str_repr = str(stats)
        
        self.assertIn("scheduler_total_time=100.000000", str_repr)
        self.assertIn("scheduler_processing_time=80.000000", str_repr)
        self.assertIn("queue_packet_processing_delays={1: 0.002, 2: 0.003}", str_repr)
        self.assertIn("user_packet_processing_delays={101: 0.001, 102: 0.004}", str_repr)
        self.assertIn("scheduler_throughput=50.500000", str_repr)

    def test_load_stats_from_yaml(self):
        """Тест загрузки данных из YAML файла"""
        stats = load_stats_from_yaml(self.temp_file.name)
        
        self.assertEqual(stats.scheduler_total_time, 100.0)
        self.assertEqual(stats.scheduler_processing_time, 80.0)
        self.assertEqual(stats.scheduler_packet_processing_delay, 0.005)
        self.assertDictEqual(stats.queue_packet_processing_delays, {1: 0.002, 2: 0.003})
        self.assertEqual(stats.scheduler_throughput, 50.5)

    def test_load_stats_from_missing_yaml(self):
        """Тест загрузки из несуществующего файла"""
        with self.assertRaises(FileNotFoundError):
            load_stats_from_yaml("non_existent_file.yaml")

    def test_load_stats_from_invalid_yaml(self):
        """Тест загрузки из некорректного YAML"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as temp_file:
            temp_file.write("invalid: yaml: content")
            temp_file.flush()
            
            with self.assertRaises(yaml.YAMLError):
                load_stats_from_yaml(temp_file.name)

    def test_load_stats_with_missing_fields(self):
        """Тест загрузки YAML с отсутствующими полями"""
        partial_data = {
            "scheduler_total_time": 100.0,
            "scheduler_processing_time": 80.0
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml') as temp_file:
            yaml.dump(partial_data, temp_file)
            temp_file.flush()
            
            stats = load_stats_from_yaml(temp_file.name)
            
            self.assertEqual(stats.scheduler_total_time, 100.0)
            self.assertEqual(stats.scheduler_processing_time, 80.0)
            self.assertEqual(stats.scheduler_throughput, 0.0)  # Должно быть значение по умолчанию
            self.assertDictEqual(stats.queue_packet_processing_delays, {})

if __name__ == '__main__':
    unittest.main()