import os
import csv
import random
import string
import time
import benchmarking
import system_diagnostics
import plotting
from settings import Settings

settings = Settings()

def hash_id():
    hash_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    return f"{hash_string}-{timestamp}"

def save_csv(results_cpu, results_gpu, cpu_cores):
    # Directory based on debug setting
    directory = "DEBUG_benchmark" if settings.debug else "RUNTIME_benchmark"
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        print(f"Warning: Directory '{directory}' does not exist. Generating it.")
        os.makedirs(directory)
    
    # Generate filename
    filename = os.path.join(directory, f"{hash_id()}.csv")
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write headers
        headers = ["Matrix Size", "Device", "Cores", "Min Time", "Avg Time", "Max Time"]
        csvwriter.writerow(headers)
        
        # Write CPU data
        for size, results in results_cpu.items():
            for core, times in zip(cpu_cores, results):
                csvwriter.writerow([size, "CPU", core, min(times), sum(times) / len(times), max(times)])
        
        # Write GPU data
        for size, times in results_gpu.items():
            csvwriter.writerow([size, "GPU", "-", min(times), sum(times) / len(times), max(times)])
    
    print(f"Results saved to: {filename}")

def list_saved_benchmarks(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    sorted_files = sorted(files, key=lambda x: x.split('-')[-2] + x.split('-')[-1], reverse=True)
    return sorted_files

def load_csv(filename, directory):
    full_path = os.path.join(directory, filename)
    results_cpu = {}
    results_gpu = {}

    with open(full_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # skip header
        for row in csvreader:
            size, device, cores, min_time, avg_time, max_time = row
            if device == "CPU":
                if int(size) not in results_cpu:
                    results_cpu[int(size)] = []
                results_cpu[int(size)].append([float(min_time), float(avg_time), float(max_time)])
            elif device == "GPU":
                results_gpu[int(size)] = [float(min_time), float(avg_time), float(max_time)]
                
    return results_cpu, results_gpu

def get_user_choice():
    return input("Do you want to run a new benchmark or load a saved one? (Enter 'run' or 'load'): ").lower()

def handle_load_choice():
    cpu_cores, _ = system_diagnostics.get_system_info()[:2]
    directory = "DEBUG_benchmark" if settings.debug else "RUNTIME_benchmark"
    
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return handle_no_benchmark_directory()

    saved_benchmarks = list_saved_benchmarks(directory)

    # Check if directory is empty
    if not saved_benchmarks:
        print("No benchmarks found in the directory.")
        return handle_no_benchmark_directory()

    print("List of saved benchmarks:")
    for i, name in enumerate(saved_benchmarks):
        print(f"{i + 1}. {name}")

    while True:
        benchmark_choice = input("Enter the number of the benchmark you want to load, or type the name of the csv: ")
        if benchmark_choice.isdigit():
            benchmark_choice = int(benchmark_choice)
            if 1 <= benchmark_choice <= len(saved_benchmarks):
                filename = saved_benchmarks[benchmark_choice - 1]
                break
            else:
                print(f"Invalid choice. Please choose a number between 1 and {len(saved_benchmarks)}.")
        else:
            filename = benchmark_choice
            if filename in saved_benchmarks:
                break
            else:
                print("Invalid filename. Please choose from the list.")

    results_cpu, results_gpu = load_csv(filename, directory)
    plotting.plotting(results_cpu, results_gpu, cpu_cores)

def handle_run_choice():
    cpu_cores, sizes_to_test, _ = system_diagnostics.get_system_info()
    system_diagnostics.print_system_info()
    results_cpu, results_gpu = benchmarking.benchmark(cpu_cores, sizes_to_test)
    save_csv(results_cpu, results_gpu, cpu_cores)
    plotting.plotting(results_cpu, results_gpu, cpu_cores)

def handle_no_benchmark_directory():
    choice = input("No benchmarks are available to load. Would you like to run a new benchmark instead? (Enter 'yes' or 'no'): ").lower()
    if choice == 'yes':
        handle_run_choice()
    else:
        print("Exiting program.")
        exit()  # exits the program