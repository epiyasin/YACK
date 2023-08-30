import system_diagnostics
import benchmarking
import plotting
from settings import Settings

settings = Settings()

def main():
    cpu_cores, sizes_to_test = system_diagnostics.print_system_info()
    results_cpu, results_gpu = benchmarking.benchmark(cpu_cores, sizes_to_test)
    plotting.plotting(results_cpu, results_gpu, cpu_cores)
    
if __name__ == "__main__":
	main()