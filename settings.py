from dataclasses import dataclass, field

@dataclass
class Settings:
    debug: bool = True
    testing: bool = True
    safety_factor: float = 0.85
    min_matrix_size: int = 1024
    warm_up_sizes: list = field(default_factory=lambda: [2048, 4096, 8192])
    sizes_to_test: list = field(default_factory=lambda: [16, 32, 64])
    debug_cores: tuple = (1, 2, 4, 8)
    figure_size: tuple = (8, 6)
    num_runs: int = 5