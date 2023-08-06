from raypipe import logger
from raypipe.core import rpipe
import tensorflow as tf

from raypipe.core.data_model import LearningConfig
from raypipe.core.rpipe.utils import build_ray_trainer, TrainReportCallback


@rpipe.init
class ModelProxy:
    def __init__(self, model_strategy_func,data_generator_func):
        """
        paras as model config
        :param kwargs:
        """
        self._validate_model(model_strategy_func)
        self._validate_learning_config(self._learning_config)

        self.model_strategy_func = model_strategy_func
        self.data_generator_func=data_generator_func

        self.ray_trainer = build_ray_trainer(self._trainer_config)

        if not self.ray_trainer: raise NotImplementedError("Trainer not built.")
        self.initialized=True

    @rpipe.is_init
    def _validate_env(self):
        if not self.initialized:
            raise EnvironmentError("Model distribution not initialized")

    def _validate_model(self,model):
        #todo
        pass

    def _validate_learning_config(self, config:LearningConfig):
        #todo
        pass

    def local_train(self,dataset):
        self._validate_env()
        local_model=self.model_strategy_func(self.learning_cfg)
        local_model.fit(dataset)

    def local_eval(self):
        pass

    def _train_template(self,general_config):
        learning_config=general_config.get("learning_config")
        trainer_config = general_config.get("trainer_config")
        data_cfg= general_config.get("data_cfg")

        global_batch_size = learning_config.batch_size * trainer_config.num_workers
        batch_dataset = self.data_generator_func(data_cfg,global_batch_size)

        strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
        with strategy.scope():
            multi_worker_model = self.model_strategy_func(learning_config.json())

        history = multi_worker_model.fit(
            batch_dataset,
            epochs=self.learning_config.epochs,
            steps_per_epoch=self.learning_config.steps_per_epoch,
            callbacks=[TrainReportCallback()])
        results = history.history
        return results

    def submit(self):
        """
        :return:
        """
        self._validate_env()
        self.ray_trainer.start()
        logger.info('=========== Trainer started =========== ')

        self.ray_trainer.run(
            train_func=self._train_template,
            config={
                    "learning_config":self._learning_config,
                    "trainer_config":self._trainer_config,
                    "data_cfg":self._data_cfg}
            )

    def upload(self):
        """
        :return:
        """
        self._validate_env()


    def collect(self):
        """
        :return:
        """
        self._validate_env()

    def shutdown(self):
        self.ray_trainer.shutdown()
        self.ray_trainer=None
        logger.info('=========== Model training ended =========== ')



