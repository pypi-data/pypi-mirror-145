from typing import Dict, Optional

from pydantic import BaseModel


class RayConfig(BaseModel):
    address:str
    redis_password:str
    runtime_env: Dict


class TrainerConfig(BaseModel):
    backend:str
    num_workers:int
    use_gpu: bool


class LearningConfig(BaseModel):
    lr:float
    batch_size:int
    epochs: int
    steps_per_epoch: int
