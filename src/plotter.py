import os
import matplotlib.pyplot as plt
from typing import Dict
from src.stats import Stats
import numpy as np

OUTPUT_DIR = "output/"

def log_draw(fn):
    def inner(*args, **kwargs):
        path = fn(*args, **kwargs)
        print(f"{fn.__name__}: Done.\n"
              f"Saved to {os.getcwd()}{path[1:]}\n")
        return

    return inner

class Plotter:
    stats: Stats
    
    def __init__(self, stats: Stats):
        self.stats = stats
        
    def run(self):
        try:
            self.draw_modelling_time_pie_chart(
                self.stats.scheduler_processing_time,
                self.stats.scheduler_idle_time,
                self.stats.scheduler_wait_time)
            
            self.draw_queue_packet_processing_delay_pie_chart(
                self.stats.scheduler_packet_processing_delay,
                self.stats.queue_packet_processing_delays)
            
            self.draw_user_packet_processing_delay_bar_chart(
                self.stats.scheduler_packet_processing_delay,
                self.stats.user_packet_processing_delays)
            
            self.draw_scheduler_throughput_bar_chart(
                self.stats.scheduler_throughput,
                self.stats.max_scheduler_throughput,
                self.stats.scheduler_unused_resources,
                1)
        except Exception as e:
            print(e)
    
    @log_draw
    def draw_queue_packet_processing_delay_pie_chart(
        self,
        scheduler_packet_processing_delay: float, 
        queue_packet_processing_delays: Dict[int, float]):
        filename = "queue_packet_processing_delay_bar_chart.png"
        path = f"./{OUTPUT_DIR}{filename}"
        
        labels = [f"Очередь {idx + 1}" for idx, _ 
                  in queue_packet_processing_delays.items()]
        labels.append("Среднее")
        
        data = [value * 1000 for _, value in queue_packet_processing_delays.items()]
        data.append(scheduler_packet_processing_delay * 1000)
        

        plt.bar(x=labels, height=data, align="center", 
                edgecolor='black')
        
        plt.tight_layout()
        plt.title("Задержка обслуживания пакетов в очередях", pad=20)
        plt.xlabel("Номер очереди")
        plt.ylabel("Задержка (мс)")
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    @log_draw  
    def draw_user_packet_processing_delay_bar_chart(
        self,
        scheduler_packet_processing_delay: float, 
        user_packet_processing_delays: Dict[int, float]):
        filename = "user_packet_processing_delay_bar_chart.png"
        path = f"./{OUTPUT_DIR}{filename}"
        
        labels = [f"Абонент {idx + 1}" for idx, _ 
                  in user_packet_processing_delays.items()]
        labels.append("Среднее")
        
        data = [value * 1000 for _, value in user_packet_processing_delays.items()]
        data.append(scheduler_packet_processing_delay * 1000)
        

        plt.bar(x=labels, height=data, align="center", 
                edgecolor='black')
        
        plt.tight_layout()
        plt.title("Задержка обслуживания пакетов пользователей", pad=20)
        plt.xlabel("Идентификатор пользователя")
        plt.ylabel("Задержка (мс)")
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path

    @log_draw
    def draw_modelling_time_pie_chart(
        self, 
        scheduler_processing_time: float,
        scheduler_idle_time: float,
        scheduler_wait_time: float):
        filename = "modelling_time_pie_chart.png"
        path = f"./{OUTPUT_DIR}{filename}"
        labels = ["Время работы", "Время простоя"]
        data = [scheduler_processing_time + scheduler_idle_time,  
                scheduler_wait_time]

        plt.pie(data, labels=labels, colors=None, 
                autopct='%1.1f%%', startangle=140, 
                wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        plt.axis('equal')
        plt.title("Время моделирования", pad=20)        
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    @log_draw
    def draw_scheduler_throughput_bar_chart(
        self, 
        scheduler_throughput: float,
        max_scheduler_throughput: float, 
        scheduler_unused_resources: float,
        max_scheduler_resources: float):
        
        filename = "scheduler_throughput_bar_chart.png"
        path = f"./{OUTPUT_DIR}{filename}"
        
        # 1. Подготовка данных
        used_throughput = scheduler_throughput 
        unused_throughput = (max_scheduler_throughput - scheduler_throughput)
        
        used_throughput_part = (used_throughput / max_scheduler_throughput) * 100
        unused_throughput_part = (unused_throughput / max_scheduler_throughput) * 100
        
        unused_resources = scheduler_unused_resources
        used_resources = (max_scheduler_resources - unused_resources)
        
        used_resources_part = (used_resources / max_scheduler_resources) * 100
        unused_resources_part = (unused_resources / max_scheduler_resources) * 100
        
        # 2. Настройки внешнего вида
        plt.figure(figsize=(8, 6))  # Увеличиваем ширину для двух столбцов
        
        # 3. Позиции столбцов на оси X
        x_positions = [0, 0.5]  # Позиции для двух групп столбцов
        bar_width = 0.25  # Ширина каждого столбца
        
        # 4. Цвета
        colors = {
            'Used': '#2ca02c',
            'Unused': '#d62728'
        }
        
        # 5. Построение столбцов для пропускной способности
        plt.bar(
            x=x_positions[0],
            height=used_throughput_part,
            width=bar_width,
            color=colors['Used'],
            edgecolor='black',
            label='Использовано'
        )
        plt.bar(
            x=x_positions[0],
            height=unused_throughput_part,
            width=bar_width,
            bottom=used_throughput_part,
            color=colors['Unused'],
            edgecolor='black',
            label='Неиспользовано'
        )
        
        # 6. Построение столбцов для ресурсных блоков
        plt.bar(
            x=x_positions[1],
            height=used_resources_part,
            width=bar_width,
            color=colors['Used'],
            edgecolor='black'
        )
        plt.bar(
            x=x_positions[1],
            height=unused_resources_part,
            width=bar_width,
            bottom=used_resources_part,
            color=colors['Unused'],
            edgecolor='black'
        )
        
        # 7. Настройка осей и подписей
        plt.ylabel('Использование (%)')
        plt.title('Использование ресурсов канала планировщиком')
        
        # Устанавливаем подписи под столбцами
        plt.xticks(x_positions, ['Пропускная способность', 'Ресурсные блоки'])
        
        # 8. Легенда
        plt.legend(
            framealpha=0.9,
            loc='upper left',
            bbox_to_anchor=(1.02, 1),
            borderaxespad=0
        )
        
        # 9. Сохранение
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path