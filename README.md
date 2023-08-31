# YACK - Yet Another Core Kinetoscope
 
This program benchmarks matrix multiplication performance on both CPU and GPU. It checks the performance based on the number of CPU cores and varying matrix sizes. The results are then plotted for visualization.

📋 Table of Contents

- [Requirements](#requirements)
- Installation
- Configuration
- Usage
- Overview of Modules
- Notes
- Contributing

## 📦 Requirements

- Python 3.x
- PyTorch
- numpy
- psutil
- tqdm
- matplotlib

## 🛠 Installation 

### 1. Clone the repository:

```bash
git clone https://github.com/epiyasin/YACK.git
```
### 2. Navigate to the repository directory:

```bash
cd path/to/repo
```

### 3. Install the required packages:
```bash
pip install torch numpy psutil tqdm matplotlib
```

## ⚙ Configuration

You can configure various settings in the `settings.py` file:

- **debug**: Enables/Disables debug mode.
- **testing**: Enables/Disables testing mode.
- **safety_factor**: Defines the portion of RAM that is considered safe for benchmarking.
- **min_matrix_size**: The minimum matrix size for the tests.
- **warm_up_sizes**: List of matrix sizes used for warming up the GPU.
- **sizes_to_test**: List of matrix sizes for testing in debug mode.
- **debug_cores**: CPU core counts to test in debug mode.
- **figure_size**: Dimensions of the resulting plot.
- **num_runs**: Number of times to repeat each test for more accurate results.

## 🚀 Usage

Run the main benchmarking script:

```bash
python main.py
```

This script will:

1. Print system information.
2. Perform benchmarking on the matrix multiplications.
3. Plot the results, showcasing the time taken for each matrix size and number of CPU cores.

## 🔍 Overview of Modules

- `settings.py`: Holds configuration data.
- `system_diagnostics.py`: Handles system-related operations, like printing system information and calculating available resources.
- `benchmarking.py`: Contains functions to perform matrix multiplications on CPU and GPU and time these operations.
- `plotting.py`: Provides functionality to plot the benchmarking results.
- `main.py`: The main script tying everything together.

## 🔔 Notes

- CUDA support: macOS users should note that recent versions of macOS don't natively support NVIDIA GPUs.
- CPU Core Count: The program leverages multiple CPU cores for benchmarking, and users are advised to close other CPU-intensive applications during the benchmarking process for accurate results.
- Windows users: Temperature-based throttling checks are not enabled on Windows.

## 🤝 Contributing

Feel free to submit pull requests or open issues if you find any bugs or have feature requests.