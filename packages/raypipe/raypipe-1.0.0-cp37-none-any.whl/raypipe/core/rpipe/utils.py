import ray
from ray.train import Trainer
import ray.train as train

from tensorflow.python.keras.callbacks import Callback
from raypipe.core.data_model import RayConfig, TrainerConfig


def start_ray(ray_config:RayConfig):
    try:
        ray.init(address=ray_config.address,
                 _redis_password=ray_config.redis_password,
                 runtime_env=ray_config.runtime_env
                 )
    except:
        ray.init()

def build_ray_trainer(trainer_cfg:TrainerConfig):
    return  Trainer(backend=trainer_cfg.backend,
                    num_workers=trainer_cfg.num_workers,
                    use_gpu=trainer_cfg.use_gpu)

class TrainReportCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        train.report(**logs)