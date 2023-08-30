import time
import torch
import os
from tqdm import tqdm  # Import the required function
from settings import Settings

settings = Settings()

def matrix_mult_on_cpu(size, num_threads):
    # Set device to CPU
    device = torch.device("cpu")

    # Generate two random matrices of size 5000x5000
    mat1 = torch.rand(size, size, device=device)
    mat2 = torch.rand(size, size, device=device)

    # Set the number of threads
    torch.set_num_threads(num_threads)

    # Time the matrix multiplication on CPU
    start_time = time.time()
    result = torch.mm(mat1, mat2)
    end_time = time.time()

    return end_time - start_time

def matrix_mult_on_gpu(size):
    # Ensure CUDA is available
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available. Ensure you have a CUDA-compatible GPU and necessary software installed.")

    # Set device to GPU
    device = torch.device("cuda:0")

    # Generate two random matrices of size 5000x5000
    mat1 = torch.rand(size, size, device=device)
    mat2 = torch.rand(size, size, device=device)

    # Time the matrix multiplication on GPU
    start_time = time.time()
    result = torch.mm(mat1, mat2)
    torch.cuda.synchronize()  # Ensure completion of the GPU task
    end_time = time.time()

    return end_time - start_time

def warm_up_gpu():
    # Use tqdm to wrap the iterable settings.warm_up_sizes
    for size in tqdm(settings.warm_up_sizes, desc="Warming up GPU", ncols=100):  # 'desc' sets the description of the progress bar
        _ = matrix_mult_on_gpu(size)  # Run multiple warm-ups with increasing sizes.

def benchmark(cpu_cores, sizes_to_test):
    
    warm_up_gpu()
    print("GPU warmed up.")

    results_cpu = {}
    results_gpu = {}
    num_runs = settings.num_runs

    for size in sizes_to_test:
        results_cpu[size] = []
        results_gpu[size] = []
        print(f"\nTesting matrix size: {size}x{size}")

        for cores in cpu_cores:
            if cores < os.cpu_count():  # Leave at least one core free
                run_times = []
                for _ in range(num_runs):
                    run_times.append(matrix_mult_on_cpu(size, cores))
                results_cpu[size].append(run_times)

                avg_time = sum(run_times) / num_runs
                min_time = min(run_times)
                max_time = max(run_times)
                print(f"  Using {cores} CPU cores. Min: {min_time:.6f} sec, Max: {max_time:.6f} sec, Avg: {avg_time:.6f} sec.")

        run_times_gpu = []
        for _ in range(settings.num_runs):
            run_times_gpu.append(matrix_mult_on_gpu(size))
        results_gpu[size] = run_times_gpu

        avg_time_gpu = sum(run_times_gpu) / num_runs
        min_time_gpu = min(run_times_gpu)
        max_time_gpu = max(run_times_gpu)
        print(f"  Using GPU. Min: {min_time_gpu:.6f} sec, Max: {max_time_gpu:.6f} sec, Avg: {avg_time_gpu:.6f} sec.")
    
    return results_cpu, results_gpu
