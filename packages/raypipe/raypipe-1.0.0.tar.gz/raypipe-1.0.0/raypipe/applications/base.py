from raypipe.core.model_proxy import ModelProxy


class BaseNN(object):
    def model_strategy_func(self):
        raise NotImplementedError("Please implement model strategy")

    def data_generator_func(self):
        raise NotImplementedError("Please implement data generator")

    def __init__(self, **general_cfg):
        if "ray_cfg" not in general_cfg:
            raise not NotImplementedError("Please configure ray_cfg")
        self._ray_cfg=general_cfg.get("ray_cfg")

        if "trainer_cfg" not in general_cfg:
            raise not NotImplementedError("Please configure trainer_cfg")
        self._trainer_cfg=general_cfg.get("trainer_cfg")

        if "learning_cfg" not in general_cfg:
            raise not NotImplementedError("Please configure learning_cfg")
        self._learning_cfg = general_cfg.get("learning_cfg")

        self._model_proxy=ModelProxy(**general_cfg)\
            (self.model_strategy_func,self.data_generator_func)

    def train(self,method="remote"):
        if method=="remote":
            self._model_proxy.submit()
        else:
            self._model_proxy.local_train()

    def serve(self,method="remote"):
        pass


