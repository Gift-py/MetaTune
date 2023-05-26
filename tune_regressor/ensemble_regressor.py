from baseline import SampleClassMixin
from optuna.trial import Trial
from dataclasses import dataclass
from typing import Iterable, Optional, Dict, Any, Union, Callable
from sklearn.ensemble import (
    RandomForestRegressor, 
    ExtraTreesRegressor, 
    AdaBoostRegressor, 
    GradientBoostingRegressor, 
    BaggingRegressor, 
    StackingRegressor,
    HistGradientBoostingRegressor,
)

@dataclass
class RandomForestRegressorTuner(SampleClassMixin):
    n_estimators_space: Iterable[int] = (1, 200)
    criterion_space: Iterable[str] = ("squared_error", "absolute_error", "friedman_mse", "poisson")
    max_depth_space: Iterable[int] = (1, 100)
    min_samples_split_space: Iterable[Union[int, float]] = (0.1, 1.0)
    min_samples_leaf_space: Iterable[Union[int, float]] = (0.1, 1.0)
    min_weight_fraction_leaf_space: Iterable[float] = (0.0, 0.5)
    max_features_space: Iterable[str] = ("sqrt", "log2", None)
    max_leaf_nodes_space: Iterable[int] = (1, 1000)
    min_impurity_decrease_space: Iterable[float] = (0.0, 1.0)
    bootstrap_space: Iterable[bool] = (True, False)
    oob_score_space: Iterable[bool] = (True, False)
    ccp_alpha_space: Iterable[float] = (0.0, 1.0)
    max_samples_space: Iterable[Union[int, float]] = (0.1, 1.0)
    model: Any = None
    
    def _sample_params(self, trial: Optional[Trial]=None) -> Dict[str, Any]:
        super()._sample_params(trial)

        is_space_type: Callable = lambda space, type : all(list(map(lambda x: isinstance(x, type), space)))
        
        params = {}
        params["n_estimators"] = trial.suggest_int("n_estimators", *self.n_estimators_space, log=False)
        params["criterion"] = trial.suggest_categorical("criterion", self.criterion_space)
        params["max_depth"] = trial.suggest_int("max_depth", *self.max_depth_space, log=False)

        if is_space_type(self.min_samples_split_space, float):
            params["min_samples_split"] = trial.suggest_float("min_samples_split", *self.min_samples_split_space, log=False)
        else:
            params["min_samples_split"] = trial.suggest_int("min_samples_split", *self.min_samples_split_space, log=False)

        if is_space_type(self.min_samples_leaf_space, float):
            params["min_samples_leaf"] = trial.suggest_float("min_samples_leaf", *self.min_samples_leaf_space, log=False)
        else:
            params["min_samples_leaf"] = trial.suggest_int("min_samples_leaf", *self.min_samples_leaf_space, log=False)

        params["min_weight_fraction_leaf"] = trial.suggest_float("min_weight_fraction_leaf", *self.min_weight_fraction_leaf_space, log=False)
        params["max_features"] = trial.suggest_categorical("max_features", self.max_features_space)
        params["max_leaf_nodes"] = trial.suggest_int("max_leaf_nodes", *self.max_leaf_nodes_space, log=False)
        params["min_impurity_decrease"] = trial.suggest_float("min_impurity_decrease", *self.min_impurity_decrease_space)
        params["bootstrap"] = trial.suggest_categorical("bootstrap", self.bootstrap_space)
        params["oob_score"] = trial.suggest_categorical("oob_score", self.oob_score_space)
        params["ccp_alpha"] = trial.suggest_float("ccp_alpha", *self.ccp_alpha_space, log=False)

        if is_space_type(self.max_samples_space, float):
            params["max_samples"] = trial.suggest_float("max_samples", *self.max_samples_space, log=False)

        else:
            params["max_samples"] = trial.suggest_int("max_samples", *self.max_samples_space, log=False)
        
        return params
    
    def sample_model(self, trial: Optional[Trial]=None) -> Any:
        super().model(trial)
        params = self._sample_params(trial)
        model = super()._evaluate_sampled_model("regression", RandomForestRegressor, params)
        self.model = model
        
        return model
    

@dataclass
class ExtraTreesRegressorTuner(RandomForestRegressorTuner):
     
    def _sample_params(self, trial: Optional[Trial]=None) -> Dict[str, Any]:
        return super(ExtraTreesRegressorTuner, self)._sample_params(trial)
    
    def sample_model(self, trial: Optional[Trial]=None) -> Any:
        super(RandomForestRegressorTuner, self).model(trial)
        params = self._sample_params(trial)
        model = super(RandomForestRegressorTuner, self)._evaluate_sampled_model("regression", ExtraTreesRegressor, params)
        self.model = model
        
        return model
    

@dataclass
class AdaBoostRegressorTuner(SampleClassMixin):
    estimator_space: Iterable[Optional[object]] = (None, )
    n_estimators_space: Iterable[int] = (1, 200)
    learning_rate_space: Iterable[float] = (0.01, 1.0)
    loss_space: Iterable[str] = ("linear", "square", "exponential")
    model: Any = None
    
    def _sample_params(self, trial: Optional[Trial]=None) -> Dict[str, Any]:
        super()._sample_params(trial)
        
        params = {}
        params["estimator"] = trial.suggest_categorical("estimator", self.estimator_space)
        params["n_estimators"] = trial.suggest_int("n_estimators", *self.n_estimators_space, log=False)
        params["learning_rate"] = trial.suggest_float("learning_rate", *self.learning_rate_space, log=False)
        params["loss"] = trial.suggest_categorical("loss", self.loss_space)
        
        return params
    
    def sample_model(self, trial: Optional[Trial]=None) -> Any:
        super().model(trial)
        params = self._sample_params(trial)
        model = super()._evaluate_sampled_model("regression", AdaBoostRegressor, params)
        self.model = model

        return model
    

@dataclass
class GradientBoostingRegressorTuner(SampleClassMixin):
    loss_space: Iterable[str] = ("squared_error", "absolute_error", "huber", "quantile")
    learning_rate_space: Iterable[float] = (0.001, 1.0)
    n_estimators_space: Iterable[int] = (1, 100)
    subsample_space: Iterable[float] = (0.1, 1.0)
    criterion_space: Iterable[str] = ("friedman_mse", "squared_error")
    min_samples_split_space: Iterable[Union[int, float]] = (0.1, 1.0)
    min_samples_leaf_space: Iterable[Union[int, float]] = (0.1, 1.0)
    min_weight_fraction_leaf_space: Iterable[float] = (0.0, 0.5)
    max_depth_space: Iterable[int] = (1, 100)
    min_impurity_decrease_space: Iterable[float] = (0.0, 1.0)
    init_space: Iterable[Optional[object]] = (None, )
    max_features_space: Iterable[str] = ("sqrt", "log2")
    alpha_space: Iterable[float] = (0.01, 1.0)
    max_leaf_nodes_space: Iterable[Optional[int]] = (1, 1000)
    validation_fraction_space: Iterable[float] = (0.0, 0.5)
    n_iter_no_change_space: Iterable[int] = (1, 100)
    tol_space: Iterable[float] = (1e-6, 1e-3)
    ccp_alpha_space: Iterable[float] = (0.0, 1.0)
    model: Any = None
    
    def _sample_params(self, trial: Optional[Trial]=None) -> Dict[str, Any]:
        super()._sample_params(trial)

        is_space_type: Callable = lambda space, type : all(list(map(lambda x: isinstance(x, type), space)))

        params = {}
        params["loss"] = trial.suggest_categorical("loss", self.loss_space)
        params["learning_rate"] = trial.suggest_float("learning_rate", *self.learning_rate_space, log=False)
        params["n_estimators"] = trial.suggest_int("n_estimators", *self.n_estimators_space, log=False)
        params["subsample"] = trial.suggest_float("subsample", *self.subsample_space, log=False)
        params["criterion"] = trial.suggest_categorical("criterion", self.criterion_space)
        if is_space_type(self.min_samples_split_space, float):
            params["min_samples_split"] = trial.suggest_float("min_samples_split", *self.min_samples_split_space, log=False)
        else:
            params["min_samples_split"] = trial.suggest_int("min_samples_split", *self.min_samples_split_space, log=False)

        if is_space_type(self.min_samples_leaf_space, float):
            params["min_samples_leaf"] = trial.suggest_float("min_samples_leaf", *self.min_samples_leaf_space, log=False)
        else:
            params["min_samples_leaf"] = trial.suggest_int("min_samples_leaf", *self.min_samples_leaf_space, log=False)

        params["min_weight_fraction_leaf"] = trial.suggest_float("min_weight_fraction_leaf", *self.min_weight_fraction_leaf_space, log=False)
        params["max_depth"] = trial.suggest_int("max_depth", *self.max_depth_space, log=False)
        params["min_impurity_decrease"] = trial.suggest_float("min_impurity_decrease", *self.min_impurity_decrease_space)
        params["init"] = trial.suggest_categorical("init", self.init_space)
        params["max_features"] = trial.suggest_categorical("max_features", self.max_features_space)
        params["alpha"] = trial.suggest_float("alpha", *self.alpha_space, log=False)
        params["max_leaf_nodes"] = trial.suggest_int("max_leaf_nodes", *self.max_leaf_nodes_space, log=False)
        params["validation_fraction"] = trial.suggest_float("validation_fraction", *self.validation_fraction_space, log=False)
        params["n_iter_no_change"] = trial.suggest_int("n_iter_no_change", *self.n_iter_no_change_space, log=False)
        params["tol"] = trial.suggest_float("tol", *self.tol_space, log=False)
        params["ccp_alpha"] = trial.suggest_float("ccp_alpha", *self.ccp_alpha_space, log=False)
        
        return params
    
    def sample_model(self, trial: Optional[Trial]=None) -> Any:
        super().model(trial)
        params = self._sample_params(trial)
        model = super()._evaluate_sampled_model("regression", GradientBoostingRegressor, params)
        self.model = model

        return model


@dataclass
class BaggingRegressorTuner(SampleClassMixin):
    estimator_space: Iterable[Optional[object]] = (None, )
    n_estimators_space: Iterable[int] = (1, 100)
    max_samples_space: Iterable[Union[int, float]] = (0.1, 1.0)
    max_features_space: Iterable[Union[int, float]] = (0.1, 1.0)
    bootstrap_space: Iterable[bool] = (True, False)
    bootstrap_features_space: Iterable[bool] = (True, False)
    oob_score_space: Iterable[bool] = (True, False)
    model: Any = None
    
    def _sample_params(self, trial: Optional[Trial]=None) -> Dict[str, Any]:
        super()._sample_params(trial)

        is_space_type: Callable = lambda space, type : all(list(map(lambda x: isinstance(x, type), space)))

        params = {}
        params["estimator"] = trial.suggest_categorical("estimator", self.estimator_space)
        params["n_estimators"] = trial.suggest_int("n_estimators", *self.n_estimators_space, log=False)

        if is_space_type(self.max_samples_space, float):
            params["max_samples"] = trial.suggest_float("max_samples", *self.max_samples_space, log=False)
        else:
            params["max_samples"] = trial.suggest_int("max_samples", *self.max_samples_space, log=False)

        if is_space_type(self.max_features_space, float):
            params["max_features"] = trial.suggest_float("max_features", *self.max_features_space, log=False)
        else:
            params["max_features"] = trial.suggest_int("max_features", *self.max_features_space, log=False)

        params["bootstrap"] = trial.suggest_categorical("bootstrap", self.bootstrap_space)
        params["bootstrap_features"] = trial.suggest_categorical("bootstrap_features", self.bootstrap_features_space)
        params["oob_score"] = trial.suggest_categorical("oob_score", self.oob_score_space)

        return params
    
    def sample_model(self, trial: Optional[Trial]=None) -> Any:
        super().model(trial)
        params = self._sample_params(trial)
        model = super()._evaluate_sampled_model("regression", BaggingRegressor, params)
        self.model = model

        return model
    

tuner_model_class_dict: Dict[str, Callable] = {
    RandomForestRegressorTuner.__name__: RandomForestRegressor,
    ExtraTreesRegressorTuner.__name__: ExtraTreesRegressor,
    AdaBoostRegressorTuner.__name__: AdaBoostRegressor,
    GradientBoostingRegressorTuner.__name__: GradientBoostingRegressor,
    BaggingRegressorTuner.__name__: BaggingRegressor,
}
