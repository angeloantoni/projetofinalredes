class DadosComputador:
    def __init__(self, cpu_count, mem_livre, disco_livre, temp_cpu):
        self.cpu_count = cpu_count
        self.mem_livre = mem_livre
        self.disco_livre = disco_livre
        self.temp_cpu = temp_cpu

    def __str__(self):
        return f"CPU: {self.cpu_count}, Mem Livre: {self.mem_livre}, Disco Livre: {self.disco_livre}, Temp CPU: {self.temp_cpu}"