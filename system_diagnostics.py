import psutil
import time
import torch
import numpy as np
import os
from settings import Settings

settings = Settings()

def get_cpu_cores(total_cores):
    # Start with powers of 2
    cores = [1]
    i = 1
    while 2 ** i <= total_cores // 2:
        cores.append(2 ** i)
        i += 1
    
    # Handle remaining cores
    if total_cores > 12:
        # Add control points for the larger core counts
        next_steps = [cores[-1] + 4, cores[-1] + 8]
        cores.extend(next_steps)

    # Fill in the gaps leading up to total_cores - 1
    step = 2
    for j in range(cores[-1] + step, total_cores, step):
        cores.append(j)

    # Ensure we don't overshoot total_cores and append total_cores - 1 if missing
    cores = [core for core in cores if core < total_cores]
    if total_cores - 1 not in cores:
        cores.append(total_cores - 1)

    return cores

def get_cuda_cores(device_index):
    # Lookup table for CUDA Cores per SM (streaming multiprocessor) for various NVIDIA GPU architectures
    # Note: This might not be complete and can vary. Update based on NVIDIA's official documentation.
    cuda_cores_per_sm = {
        (3, 0): 192,
        (3, 5): 192,
        (3, 7): 192,
        (5, 0): 128,
        (5, 1): 128,
        (5, 2): 128,
        (6, 0): 64,
        (6, 1): 128,
        (6, 2): 128,
        (7, 0): 64,
        (7, 5): 64,
        (8, 0): 64,
        (8, 6): 128  # Add more architectures as needed
    }

    if not torch.cuda.is_available():
        raise ValueError("CUDA is not available on this system.")

    cc = torch.cuda.get_device_capability(device_index)
    sm_count = torch.cuda.get_device_properties(device_index).multi_processor_count
    cores = cuda_cores_per_sm.get(cc)

    if cores:
        return cores * sm_count
    else:
        return None  # Unknown GPU architecture

def available_ram_gb():
    return psutil.virtual_memory().available / (1024 ** 3)

def max_safe_matrix_size(dtype_size=4):
    ram_gb = available_ram_gb() * settings.safety_factor  
    max_size = int((ram_gb * (1024 ** 3) / (3 * dtype_size)) ** 0.5)
    return max_size

def get_system_info():
    cpu_cores = get_cpu_cores(os.cpu_count())
    if settings.debug:
        cpu_cores = [core for core in cpu_cores if core in settings.debug_cores]

    total_ram = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
    max_matrix = max_safe_matrix_size()
    sizes_to_test = [2 ** i for i in range(int(np.log2(settings.min_matrix_size)), int(np.log2(max_matrix)) + 1)]

    if settings.debug:
        sizes_to_test = settings.sizes_to_test

    return cpu_cores, sizes_to_test, total_ram

def print_system_info():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Get system info
    cpu_cores, sizes_to_test, total_ram = get_system_info()
    
    # Print the number of CPU core sets that will be tested
    if settings.debug:
        print(f"DEBUG MODE: Testing only the following CPU cores: {cpu_cores}")
    
    print(f"Total CPU cores available: {os.cpu_count()}")
    print(f"CPU cores to be tested: {cpu_cores}")

    # Print number of CUDA cores in the GPU
    if torch.cuda.is_available():
        total_cuda_cores = get_cuda_cores(0)
        if total_cuda_cores:
            print(f"Total CUDA cores available on the GPU: {total_cuda_cores}")
        else:
            print("Unable to detect the total number of CUDA cores on the GPU.")

    # Print total RAM available
    ram_for_benchmark = total_ram * settings.safety_factor  # Considering the safety factor
    print(f"Total RAM available: {total_ram:.2f} GB")
    print(f"Total RAM to be used for the benchmark: {ram_for_benchmark:.2f} GB")

    # Print matrix sizes that will be tested
    if settings.debug:
        print(f"DEBUG MODE: Testing only the following matrix sizes: {sizes_to_test}")

    print(f"Matrix sizes to be tested: {sizes_to_test}")
    print(f"Number of iterations to run per calculation: {settings.num_runs}")
    
    # Ask the user to close other programs to reduce core load
    print("\nPlease close as many programs as possible to minimize external load on the CPU cores.")
    input("\nOnce ready, press Enter to continue...") 

    # Countdown from 5 to 0
    for i in range(5, 0, -1):
        print(f"\rStarting benchmarking in: {i}", end='', flush=True)
        time.sleep(1)

    print("\rStarting benchmarking now...") 

    print("\nWarning: Temperature-based throttling checks are not enabled on Windows.")
    
    return cpu_cores, sizes_to_test
