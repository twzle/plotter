import yaml
from typing import Dict

class Stats:
    def __init__(self, scheduler_total_time: float,
             scheduler_processing_time: float,
             scheduler_idle_time: float,
             scheduler_wait_time: float,
             scheduler_packet_processing_delay: float,
             queue_packet_processing_delays: Dict[int, float],
             user_packet_processing_delays: Dict[int, float],
             scheduler_throughput: float,
             max_scheduler_throughput: float,
             scheduler_unused_resources: float):
        ''' 
        Initialize statistics container.
        
        Args:
            scheduler_total_time: Total scheduler operation time
            scheduler_processing_time: Time spent processing packets
            scheduler_idle_time: Time spent idle
            scheduler_wait_time: Time spent waiting
            scheduler_packet_processing_delay: Average packet processing delay
            queue_packet_processing_delays: Delays per queue
            user_packet_processing_delays: Delays per user
            scheduler_throughput: Average throughput
            max_scheduler_throughput: Maximum theoretical throughput
            scheduler_unused_resources: Part of unused resources from maximum
        '''
        self.scheduler_total_time = scheduler_total_time
        self.scheduler_processing_time = scheduler_processing_time
        self.scheduler_idle_time = scheduler_idle_time
        self.scheduler_wait_time = scheduler_wait_time
        self.scheduler_packet_processing_delay = scheduler_packet_processing_delay
        self.queue_packet_processing_delays = queue_packet_processing_delays
        self.user_packet_processing_delays = user_packet_processing_delays
        self.scheduler_throughput = scheduler_throughput
        self.max_scheduler_throughput = max_scheduler_throughput
        self.scheduler_unused_resources = scheduler_unused_resources

    def __str__(self):
        return (f"Stats:\n"
                f"scheduler_total_time={self.scheduler_total_time:.6f}, \n"
                f"scheduler_processing_time={self.scheduler_processing_time:.6f}, \n"
                f"scheduler_idle_time={self.scheduler_idle_time:.6f}, \n"
                f"scheduler_wait_time={self.scheduler_wait_time:.6f}, \n"
                f"scheduler_packet_processing_delay={self.scheduler_packet_processing_delay:.6f}, \n"
                f"queue_packet_processing_delays={self.queue_packet_processing_delays}, \n"
                f"user_packet_processing_delays={self.user_packet_processing_delays}, \n"
                f"scheduler_throughput={self.scheduler_throughput:.6f}, \n"
                f"max_scheduler_throughput={self.max_scheduler_throughput:.6f}, \n"
                f"scheduler_unused_resources={self.scheduler_unused_resources:.6f})")

# Импорт данных из YAML в объект класса Stats
def load_stats_from_yaml(file_path: str) -> Stats:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    return Stats(
        scheduler_total_time=
            data.get("scheduler_total_time", 0.0),
        scheduler_processing_time=
            data.get("scheduler_processing_time", 0.0),
        scheduler_idle_time=
            data.get("scheduler_idle_time", 0.0),
        scheduler_wait_time=
            data.get("scheduler_wait_time", 0.0),
        scheduler_packet_processing_delay=
            data.get("scheduler_packet_processing_delay", 0.0),
        queue_packet_processing_delays=
            data.get("queue_packet_processing_delays", {}),
        user_packet_processing_delays=
            data.get("user_packet_processing_delays", {}),
        scheduler_throughput=
            data.get("scheduler_throughput", 0.0),
        max_scheduler_throughput=
            data.get("max_scheduler_throughput", 0.0), 
        scheduler_unused_resources=
            data.get("scheduler_unused_resources", 0.0), 
    )