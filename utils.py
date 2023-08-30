import os
import csv
import random
import string
import time
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
