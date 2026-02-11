class Process:
    def __init__(self, pid: int, max_resources: list[int]):
        """
        Initializes a process with its unique process ID and maximum resources it needs.
        """
        self.pid = pid
        self.max = max_resources.copy()
        self.allocation = [0] * len(max_resources) 
        self.need = self.max.copy()
        self.requested = [0] * len(max_resources) 
        self.status = "ready" 

    def allocate(self, resources: list[int]):
        """
        Allocates resources to this process and updates its need.
        """
        for i in range(len(resources)):
            self.allocation[i] += resources[i]
            self.need[i] = self.max[i] - self.allocation[i] 

    def request(self, resources: list[int]):
        """
        Request resources for the process.
        """
        self.requested = resources.copy()
        
    def __str__(self):
        """For printing the process"""
        return f"P{self.pid} | Alloc: {self.allocation} | Need: {self.need} | Req: {self.requested} | Status: {self.status}"
