from typing import List, Set, Tuple

# FIX: All imports are now relative (from the current CORE package)
from .Bankers import Banker # Assuming Banker.py exists
from .process import Process 
from .resource import Resource 

class System:
    def __init__(self, resource_totals: List[int]):
        """Simulates an OS managing processes and resources."""
        self.resources = [Resource(rid, total) for rid, total in enumerate(resource_totals)]
        self.processes: List[Process] = [] 
        self.available = resource_totals.copy()

    # FIX: Corrected arguments to match FRONTEND/app.py logic
    def add_process(self, pid: int, max_needs: List[int], initial_allocation: List[int]):
        """Registers a process and its initial allocation."""
        
        process = Process(pid, max_needs)
        
        # Allocate resources to the process and update system availability
        for r, units in enumerate(initial_allocation):
            if units > 0:
                # Update process allocation and system resource objects
                process.allocate([units] if len(max_needs) == 1 else [0]*r + [units] + [0]*(len(max_needs)-r-1))
                self.resources[r].allocate(units)

        # Ensure process list is large enough and insert the process at its PID
        while len(self.processes) <= pid:
            self.processes.append(None)
        
        self.processes[pid] = process
        
        # Update system-wide available list
        self.available = [r.available for r in self.resources]


    def is_safe(self, terminated_pids: List[int]) -> Tuple[bool, List[int]]:
        """
        Checks if the current state of the system is safe using Banker's Algorithm (Safety Check).
        This logic is directly embedded here from Banker.is_safe_state.
        """
        
        # Filter out terminated processes
        active_processes = [p for p in self.processes if p is not None and p.pid not in terminated_pids]
        
        current_available = [r.available for r in self.resources]
        max_needs_matrix = [p.max for p in active_processes]
        allocated_matrix = [p.allocation for p in active_processes]
        
        if not active_processes:
            return True, []
            
        # 1. Calculate Need Matrix (Max - Allocated)
        need_matrix = []
        for p in active_processes:
            need_matrix.append(p.need)
            
        # 2. Safety Check Simulation
        work = current_available[:]
        finish = [False] * len(active_processes)
        safe_sequence = []
        
        while len(safe_sequence) < len(active_processes):
            progress_made = False
            for i in range(len(active_processes)):
                if not finish[i]:
                    can_finish = True
                    for j in range(len(current_available)):
                        if need_matrix[i][j] > work[j]:
                            can_finish = False
                            break
                            
                    if can_finish:
                        # Process finishes and releases its resources
                        work = [work[j] + allocated_matrix[i][j] for j in range(len(current_available))]
                        finish[i] = True
                        safe_sequence.append(active_processes[i].pid)
                        progress_made = True
                        break 
            
            if not progress_made:
                break 
                
        is_safe = all(finish)
        return is_safe, safe_sequence

    # Placeholders for other methods
    def request_resources(self, pid: int, request: List[int]) -> bool:
        return False 

    def release_resources(self, pid: int):
        pass

    def print_state(self):
        pass
