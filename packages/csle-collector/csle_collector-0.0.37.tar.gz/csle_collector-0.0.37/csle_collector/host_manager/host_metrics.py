from typing import Dict, Any
import time
import csle_collector.host_manager.host_manager_pb2


class HostMetrics:
    """
    DTO class containing host metrics
    """

    def __init__(self, num_logged_in_users: int = 0, num_failed_login_attempts: int = 0,
                 num_open_connections: int = 0,
                 num_login_events: int = 0, num_processes: int = 0, num_users: int = 0,
                 ip: str = None, ts: float = None) -> None:
        """
        Initializes the DTO

        :param num_logged_in_users: the number of logged in users
        :param num_failed_login_attempts: the number of failed login attempts
        :param num_open_connections: the number of open connections
        :param num_login_events: the number of login events
        :param num_processes: the number of processes
        :param num_users: the number of users
        """
        self.num_logged_in_users = num_logged_in_users
        self.num_failed_login_attempts = num_failed_login_attempts
        self.num_open_connections = num_open_connections
        self.num_login_events = num_login_events
        self.num_processes = num_processes
        self.num_users = num_users
        self.ts = ts
        self.ip = ip

    def to_dto(self, ip: str) -> csle_collector.host_manager.host_manager_pb2.HostMetricsDTO:
        """
        Converts the object into a gRPC DTO for serialization

        :param ip: the ip to add to the DTO in addition to the metrics
        :return: a csle_collector.host_manager.host_manager_pb2.HostMetricsDTO
        """
        ts = time.time()
        return csle_collector.host_manager.host_manager_pb2.HostMetricsDTO(
            num_logged_in_users = self.num_logged_in_users,
            num_failed_login_attempts = self.num_failed_login_attempts,
            num_open_connections = self.num_open_connections,
            num_login_events = self.num_login_events,
            num_processes = self.num_processes,
            num_users = self.num_users,
            ip = ip,
            timestamp = ts
        )

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a Kafka record string

        :param ip: the IP to add to the record in addition to the metrics
        :return: a comma separated string representing the kafka record
        """
        ts = time.time()
        record_str = f"{ts},{ip},{self.num_logged_in_users},{self.num_failed_login_attempts}," \
                     f"{self.num_open_connections},{self.num_login_events},{self.num_processes},{self.num_users}"
        return record_str

    @staticmethod
    def from_kafka_record(record: str) -> "HostMetrics":
        """
        Converts the Kafka record string to a DTO

        :param record: the kafka record
        :return: the created DTO
        """
        parts = record.split(",")
        obj = HostMetrics(
            ip = record[1], ts=float(parts[0]),
            num_logged_in_users=int(parts[2]), num_failed_login_attempts=int(parts[3]),
            num_open_connections=int(parts[4]),
            num_login_events=int(parts[5]), num_processes=int(parts[6]), num_users=int(parts[7])
        )
        return obj

    def update_with_kafka_record(self, record: str, ip: str) -> None:
        """
        Updates the DTO based on a kafka record

        :param record: the kafka record
        :param ip: the host ip
        :return: None
        """
        parts = record.split(",")
        if parts[1] == ip:
            self.ip = parts[1]
            self.ts=float(parts[0]),
            self.num_logged_in_users=int(parts[2])
            self.num_failed_login_attempts=int(parts[3])
            self.num_open_connections=int(parts[4])
            self.num_login_events=int(parts[5])
            self.num_processes=int(parts[6])
            self.num_users=int(parts[7])

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"num_logged_in_users:{self.num_logged_in_users}, " \
               f"num_failed_login_attempts: {self.num_failed_login_attempts}, " \
               f"num_open_connections:{self.num_open_connections}, " \
               f"num_login_events:{self.num_login_events}, num_processes: {self.num_processes}," \
               f"num_users: {self.num_users}"

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HostMetrics":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = HostMetrics(
            num_logged_in_users=d["num_logged_in_users"],
            num_failed_login_attempts=d["num_failed_login_attempts"],
            num_open_connections=d["num_open_connections"],
            num_login_events=d["num_login_events"],
            num_processes=d["num_processes"],
            num_users=d["num_users"],
            ip=d["ip"],
            ts=d["ts"],
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the instance
        """
        d = {}
        d["num_logged_in_users"] = self.num_logged_in_users
        d["num_failed_login_attempts"] = self.num_failed_login_attempts
        d["num_open_connections"] = self.num_open_connections
        d["num_login_events"] = self.num_login_events
        d["num_processes"] = self.num_processes
        d["num_users"] = self.num_users
        d["ts"] = self.ts
        d["ip"] = self.ip
        return d

    def copy(self) -> "HostMetrics":
        """
        :return: a copy of the object
        """
        c = HostMetrics(
            num_logged_in_users=self.num_logged_in_users, num_failed_login_attempts=self.num_failed_login_attempts,
            num_open_connections=self.num_open_connections, num_login_events=self.num_login_events,
            num_processes=self.num_processes, num_users=self.num_users, ip=self.ip, ts=self.ts
        )
        return c

