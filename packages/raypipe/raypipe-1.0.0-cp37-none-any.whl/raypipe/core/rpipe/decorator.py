import ray

from raypipe import logger
from raypipe.core.data_model import RayConfig, TrainerConfig, LearningConfig
from raypipe.core.rpipe.utils import start_ray


def init(cls):
    default_ray_cfg = {"address": "auto",
                       "redis_password": 5241590000000000,
                       "runtime_env": {}}
    default_trainer_cfg = {"backend": "tensorflow", "num_workers": 1, "use_gpu": False}
    default_learning_cfg = {"lr": 1e-5, "batch_size": 16, "epochs": 3, "steps_per_epoch": 10}

    def wrapper(*args, **general_cfg):
        ray_cfg = general_cfg.get("ray_cfg")
        trainer_cfg = general_cfg.get("trainer_cfg")
        learning_cfg = general_cfg.get("learning_cfg")
        data_cfg=general_cfg.get("data_cfg",{})

        if not ray_cfg:
            start_ray(RayConfig(**default_ray_cfg))

        if not ray.is_initialized() and ray_cfg:
            start_ray(RayConfig(**ray_cfg))
        logger.info('=========== Ray engine prepared =========== ')

        if not trainer_cfg:
            trainer_config = TrainerConfig(**default_trainer_cfg)
        else:
            trainer_config = TrainerConfig(**trainer_cfg)

        if not learning_cfg:
            learning_config = LearningConfig(**default_learning_cfg)
        else:
            learning_config = LearningConfig(**learning_cfg)

        cls._trainer_config = trainer_config
        cls._learning_config = learning_config
        cls._data_cfg=data_cfg

        logger.info('=========== %s initialized=========== ' % cls.__name__)
        return cls

    return wrapper


def is_init(func):
    def wrapper(self):
        if not ray.is_initialized:
            raise EnvironmentError("Ray session not initialized")
        return func

    return wrapper
