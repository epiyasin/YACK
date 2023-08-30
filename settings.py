from dataclasses import dataclass, field

@dataclass
class Settings:
    debug: bool = True
    testing: bool = True
    safety_factor: float = 0.85
    min_matrix_size: int = 512
    warm_up_sizes: list = field(default_factory=lambda: [1024, 2048, 4096, 8192])
    debug_cores: tuple = (1, 2, 4, 8)
    figure_size: tuple = (8, 6)
    num_runs: int = 5
 
settings = Settings()