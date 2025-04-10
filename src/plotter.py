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
              f"Saved to {os.getcwd()}{path[1:]}")
        return

    return inner

class Plotter:
    stats: Stats
    
    def __init__(self, stats: Stats):
        self.stats = stats
        
    def run(self):
        try:
            print("MODELLING TIME")
            self.draw_modelling_time_pie_chart(
                self.stats.scheduler_processing_time,
                self.stats.scheduler_idle_time,
                self.stats.scheduler_wait_time)
            print("QUEUE DELAYS")
            self.draw_queue_packet_processing_delay_pie_chart(
                self.stats.scheduler_packet_processing_delay,
                self.stats.queue_packet_processing_delays)
            self.draw_user_packet_processing_delay_bar_chart(
                self.stats.scheduler_packet_processing_delay,
                self.stats.user_packet_processing_delays)
            self.draw_scheduler_throughput_bar_chart(
                self.stats.scheduler_throughput,
                self.stats.max_scheduler_throughput)
        except Exception as e:
            print(e)
    
    @log_draw
    def draw_queue_packet_processing_delay_pie_chart(
        self,
        scheduler_packet_processing_delay: float, 
        queue_packet_processing_delays: Dict[int, float]):
        filename = "queue_packet_processing_delay_bar_chart.png"
        path = f"./{OUTPUT_DIR}{filename}"
        
        labels = [f"Queue {idx + 1}" for idx, _ 
                  in queue_packet_processing_delays.items()]
        labels.append("Scheduler")
        
        data = [value * 1000 for _, value in queue_packet_processing_delays.items()]
        data.append(scheduler_packet_processing_delay * 1000)
        

        plt.bar(x=labels, height=data, align="center", 
                edgecolor='black')
        
        plt.tight_layout()
        plt.title("Queue packet processing delay time", pad=20)
        plt.xlabel("Queue")
        plt.ylabel("Delay (ms)")
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
        
        labels = [f"User {idx + 1}" for idx, _ 
                  in user_packet_processing_delays.items()]
        labels.append("Scheduler")
        
        data = [value * 1000 for _, value in user_packet_processing_delays.items()]
        data.append(scheduler_packet_processing_delay * 1000)
        

        plt.bar(x=labels, height=data, align="center", 
                edgecolor='black')
        
        plt.tight_layout()
        plt.title("User packet processing delay time", pad=20)
        plt.xlabel("User")
        plt.ylabel("Delay (ms)")
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
        labels = ["Processing time", "Idle time", "Wait time"]
        data = [scheduler_processing_time, 
                scheduler_idle_time, 
                scheduler_wait_time]

        plt.pie(data, labels=labels, colors=None, 
                autopct='%1.1f%%', startangle=140, 
                wedgeprops={'edgecolor': 'black', 'linewidth': 1})
        plt.axis('equal')
        plt.title("Modelling time proportions", pad=20)        
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
    
    @log_draw
    def draw_scheduler_throughput_bar_chart(
        self, 
        scheduler_throughput: float,
        max_scheduler_throughput: float):
        
        filename = "scheduler_throughput_stacked.png"
        path = f"./{OUTPUT_DIR}{filename}"
        
        # 1. Подготовка данных
        used = scheduler_throughput * 1000  # Использованная пропускная способность
        unused = (max_scheduler_throughput - scheduler_throughput) * 1000  # Неиспользованная
        
        # 2. Настройки внешнего вида
        plt.figure(figsize=(8, 6))  # Узкий график (ширина 4, высота 6)
        
        # 3. Цвета (можно использовать HEX или названия)
        colors = {
            'Used': '#2ca02c',  # Зелёный для использованной части
            'Unused': '#d62728'  # Красный для неиспользованной
        }
        
        # 4. Построение столбца с накоплением
        plt.bar(
            x=['Throughput'],  # Один столбец
            height=used,
            width=0.2,  # Сужаем ширину столбца (по умолчанию 0.8)
            color=colors['Used'],
            edgecolor='black',
            linewidth=1,
            label=f'Used: {used:.1f} Mbit/s'
        )
        
        plt.bar(
            x=['Throughput'],
            height=unused,
            width=0.2,  # Такая же ширина для совпадения
            bottom=used,  # Накопление поверх used
            color=colors['Unused'],
            edgecolor='black',
            linewidth=1,
            label=f'Unused: {unused:.1f} Mbit/s'
        )
        
        # 5. Настройка осей и подписей
        plt.ylabel('Throughput (Mbit/s)')
        plt.title('Scheduler Throughput Utilization')
        plt.xticks(rotation=45)  # Наклон подписи если нужно
        
        # 6. Легенда с прозрачным фоном
        plt.legend(
            framealpha=0.9,  # Прозрачность фона
            loc='upper right'  # Позиция
        )
        
        # 7. Сохранение
        plt.tight_layout()
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return path
