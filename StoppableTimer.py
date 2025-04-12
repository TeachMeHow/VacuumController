import threading
import time

class StoppableTimer:
    CODE_LENGTH = 4
    UPDATE_INTERVAL_S = 0.1
    
    def  __init__(self, time_s):
        self.time_left_ns = time_s * 1000 * 1000 * 1000
        self.timer_thread = threading.Thread(target=self.run_timer)
        self._state = 'READY'
        self._lock = threading.Lock()
        self.event = threading.Event()
        self._time_factor = 0
    
    def start(self):
        with self._lock:
            if not self.timer_thread.is_alive():
                self.timer_thread.run()
            self.time_factor = 1
            self._state = 'RUNNING'
    
    def pause(self):
        self.state = "PAUSED"
    
    def stop(self):
        self.state = "STOPPED"
    
            
    def _update_time_factor(self):
        if self._state == "READY" or self._state == "WAITING":
            self._time_factor = 0
        if self._state == "RUNNING":
            self._time_factor = 1
        if self._state == "PAUSED":
            self._time_factor = 0.5
        if self._state == "STOPPED":
            self._time_factor = 0
            self.remaining_time_ns = 0
            self.event.set()
    
    def get_event(self) -> threading.Event:
        return self.event
        
    @property
    def remaining_time_ns(self):
        with self._lock:
            return self.time_left_ns
        
    @property
    def time_factor(self):
        with self._lock:
            return self._time_factor
    
    @property
    def state(self):
        with self._lock:
            return self._state

    @state.setter
    def state(self, state):
        with self._lock:
            self._state = state
            self._update_time_factor()
        self.state = "READY"
    
    def run_timer(self):
        last_timestamp_ns = time.time_ns()
        time_start_ns = last_timestamp_ns
        print("timer started seconds left", self.time_left_ns // (1000 * 1000 * 1000))
        while self.time_left_ns >= 0:
            
            if self.state == "READY":
                time_start_ns = time.time_ns()
            real_elapsed_s = (time.time_ns() - time_start_ns) // (1000 * 1000 * 1000)
            tp_ns = time.time_ns() - last_timestamp_ns
            last_timestamp_ns = time.time_ns()
            print(f"state : {self.state} - real : {real_elapsed_s} - timer : {self.time_left_ns // (1000 * 1000 * 1000)}")
            self.time_left_ns -= tp_ns * self.time_factor
            time.sleep(self.UPDATE_INTERVAL_S)
        self.state = 'STOPPED'
        self.event.set()
    
