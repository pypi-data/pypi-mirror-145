"""
This module contains auto machine learning API.

The following classes are available:

    * :class:`AutomaticClassification`
    * :class:`AutomaticRegression`
    * :class:`Preprocessing`

"""
#pylint: disable=too-many-branches
#pylint: disable=too-many-statements
#pylint: disable=too-many-locals
#pylint: disable=line-too-long
#pylint: disable=too-few-public-methods
#pylint: disable=consider-using-f-string
#pylint: disable=too-many-instance-attributes
#pylint: disable=attribute-defined-outside-init
#pylint: disable=protected-access
#pylint: disable=no-self-use
#pylint: disable=consider-iterating-dictionary
import json
import logging
import os
import uuid


try:
    import pyodbc
except ImportError as error:
    pass
import pandas as pd
from hdbcli import dbapi

from hana_ml.dataframe import DataFrame
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.algorithms.pal.pal_base import (
    PALBase,
    ParameterTable,
    pal_param_register,
    try_drop,
    require_pal_usable
)
from hana_ml.ml_base import ListOfStrings
from hana_ml.algorithms.pal.preprocessing import FeatureNormalizer
from hana_ml.algorithms.pal.preprocessing import KBinsDiscretizer
from hana_ml.algorithms.pal.preprocessing import Imputer
from hana_ml.algorithms.pal.preprocessing import Discretize
from hana_ml.algorithms.pal.preprocessing import MDS
from hana_ml.algorithms.pal.preprocessing import SMOTE
from hana_ml.algorithms.pal.preprocessing import SMOTETomek
from hana_ml.algorithms.pal.preprocessing import TomekLinks
from hana_ml.algorithms.pal.preprocessing import Sampling
from hana_ml.algorithms.pal.preprocessing import FeatureSelection
from hana_ml.algorithms.pal.decomposition import PCA
from hana_ml.algorithms.pal.sqlgen import trace_sql
from hana_ml.visualizers.digraph import Digraph

logger = logging.getLogger(__name__)#pylint: disable=invalid-name


class _AutoMLBase(PALBase):
    _category_map = {"DT_Classifier": "Classifier",
                     "HGBT_Classifier": "Classifier",
                     "M_LOGR_Classifier": "Classifier",
                     "MLP_Classifier": "Classifier",
                     "NB_Classifier": "Classifier",
                     "RDT_Classifier": "Classifier",
                     "SVM_Classifier": "Classifier",
                     "DT_Regressor": "Regressor",
                     "EXP_Regressor": "Regressor",
                     "GEO_Regressor": "Regressor",
                     "GLM_Regressor": "Regressor",
                     "HGBT_Regressor": "Regressor",
                     "LOG_Regressor": "Regressor",
                     "MLP_Regressor": "Regressor",
                     "MLR_Regressor": "Regressor",
                     "POL_Regressor": "Regressor",
                     "RDT_Regressor": "Regressor",
                     "SVM_Regressor": "Regressor",
                     "FS_supervised": "Transformer",
                     "FS_unsupervised": "Transformer",
                     "CATPCA": "Transformer",
                     "PCA": "Transformer",
                     "SCALE": "Transformer",
                     "IMPUTER": "Transformer",
                     "DISCRETIZE": "Transformer",
                     "MDS": "Transformer",
                     "LabelEncoder": "Transformer",
                     "OneHotEncoder": "Transformer",
                     "SAMPLING": "Resampler",
                     "SMOTE": "Resampler",
                     "SMOTETomek": "Resampler",
                     "TomekLinks": "Resampler"}

    def __init__(self,
                 scorings=None,
                 generations=None,
                 population_size=None,
                 offspring_size=None,
                 elite_number=None,
                 min_layer=None,
                 max_layer=None,
                 mutation_rate=None,
                 crossover_rate=None,
                 random_seed=None,
                 config_dict=None,
                 progress_indicator_id=None,
                 fold_num=None,
                 resampling_method=None,
                 max_eval_time_mins=None,
                 early_stop=None):
        super(_AutoMLBase, self).__init__()
        if not hasattr(self, 'hanaml_parameters'):
            setattr(self, 'hanaml_parameters', pal_param_register())
        self.scorings = self._arg('scorings', scorings, dict)
        if self.scorings:
            self.scorings = json.dumps(self.scorings)
        self.generations = self._arg('generations', generations, int)
        self.population_size = self._arg('population_size', population_size, int)
        self.offspring_size = self._arg('offspring_size', offspring_size, int)
        self.elite_number = self._arg('elite_number', elite_number, int)
        self.min_layer = self._arg('min_layer', min_layer, int)
        self.max_layer = self._arg('max_layer', max_layer, int)
        self.mutation_rate = self._arg('mutation_rate', mutation_rate, float)
        self.crossover_rate = self._arg('crossover_rate', crossover_rate, float)
        self.random_seed = self._arg('random_seed', random_seed, int)
        self.config_dict = self._arg('config_dict', config_dict, str)
        self.progress_indicator_id = self._arg('progress_indicator_id', progress_indicator_id, str)
        self.fold_num = self._arg('fold_num', fold_num, int)
        self.resampling_method = self._arg('resampling_method', resampling_method, str)
        self.max_eval_time_mins = self._arg('max_eval_time_mins', max_eval_time_mins, float)
        self.early_stop = self._arg('early_stop', early_stop, int)
        self._status = 0
        self.__enable_workload_class = False
        self.used_workload_class_name = None

    def enable_workload_class(self, workload_class_name):
        """
        HANA WORKLOAD CLASS is recommended to set when the automatic classification or regression is called.

        Parameters
        ----------
        workload_class_name : str
            The name of HANA WORKLOAD CLASS.
        """
        self.apply_with_hint('WORKLOAD_CLASS("{}")'.format(workload_class_name), True)
        self.__enable_workload_class = True
        self.used_workload_class_name = workload_class_name

    def disable_workload_class_check(self):
        """
        Disable the workload class check. Please note that the automatic classification or regression may cause large resource.
        Without setting workload class, there's no resource restriction on the training process.
        """
        self.__enable_workload_class = True
        self.used_workload_class_name = None

    def get_workload_classes(self, connection_context):
        """
        Return the available workload classes information.
        """
        return connection_context.sql("SELECT * FROM WORKLOAD_CLASSES").collect()

    @trace_sql
    def fit(self, data, pipeline=None):
        r"""
        Fit function for AutoML.

        Parameters
        ----------
        data : DataFrame
            The training data. The structure is as follow:

            - 1st column: ID column.
            - Last column: Label column. please cast the label column to be "VARCHAR" or "NVARCHAR" if AutomaticClassification is used.
            - The rest of columns: features.

        pipeline : str or dict, optional
            Directly use the input pipeline to fit.

        Returns
        -------
        A fitted(AutomaticClassification or AutomaticRegression) object.
        """
        if not self.__enable_workload_class:
            self._status = -1
            raise FitIncompleteError("Please define the workload class and call enable_workload_class.")
        if not isinstance(data, DataFrame):
            self._status = -1
            raise TypeError("The type of data should be HANA DataFrame.")
        setattr(self, 'hanaml_fit_params', pal_param_register())
        data.connection_context.connection_id = data.connection_context.get_connection_id()
        setattr(self, "fit_data", data)
        conn = data.connection_context
        require_pal_usable(conn)
        conn.sql_tracer.set_sql_trace(self, self.__class__.__name__, 'Fit')
        if self.__enable_workload_class:
            if self.used_workload_class_name not in self.get_workload_classes(conn)["WORKLOAD_CLASS_NAME"].to_list():
                logger.warning("The workload class name cannot be found in the HANA settings.")
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        outputs = ['BEST_PIPELINE', 'MODEL', 'INFO']
        outputs = ['#PAL_AUTOML_{}_TBL_{}_{}'.format(name, self.id, unique_id)
                   for name in outputs]
        best_pipeline_tbl, model_tbl, info_tbl = outputs
        ptype = "regressor" if isinstance(self, AutomaticRegression) else 'classifier'
        param_rows = [('SCORINGS', None, None, self.scorings),
                      ('GENERATIONS', self.generations, None, None),
                      ('POPULATION_SIZE', self.population_size, None, None),
                      ('OFFSPRING_SIZE', self.offspring_size, None, None),
                      ('ELITE_NUMBER', self.elite_number, None, None),
                      ('MIN_LAYER', self.min_layer, None, None),
                      ('MAX_LAYER', self.max_layer, None, None),
                      ('MUTATION_RATE', None, self.mutation_rate, None),
                      ('CROSSOVER_RATE', None, self.crossover_rate, None),
                      ('RANDOM_SEED', self.random_seed, None, None),
                      ('CONFIG_DICT', None, None, self.config_dict),
                      ('PROGRESS_INDICATOR_ID', None, None, self.progress_indicator_id),
                      ('FOLD_NUM', self.fold_num, None, None),
                      ('PIPELINE_TYPE', None, None, ptype),
                      ('RESAMPLING_METHOD', None, None, self.resampling_method),
                      ('MAX_EVAL_TIME_MINS', None, self.max_eval_time_mins, None)]
        try:
            if pipeline:
                if isinstance(pipeline, dict):
                    pipeline = json.dumps(pipeline)
                pipeline_param = [('PIPELINE', None, None, pipeline)]
                pipeline_outputs = outputs[1:]
                self._call_pal_auto(conn,
                                    'PAL_PIPELINE_FIT',
                                    data,
                                    ParameterTable().with_data(pipeline_param),
                                    *pipeline_outputs)
            else:
                self._call_pal_auto(conn,
                                    'PAL_AUTOML_FIT',
                                    data,
                                    ParameterTable().with_data(param_rows),
                                    *outputs)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            if pipeline:
                try_drop(conn, pipeline_outputs)
            else:
                try_drop(conn, outputs)
            self._status = -1
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            if pipeline:
                try_drop(conn, pipeline_outputs)
            else:
                try_drop(conn, outputs)
            self._status = -1
            raise
        # pylint: disable=attribute-defined-outside-init
        self._status = 1
        if pipeline is None:
            self.best_pipeline_ = conn.table(best_pipeline_tbl)
        self.model_ = conn.table(model_tbl)
        self.info_ = conn.table(info_tbl)
        return self

    @trace_sql
    def predict(self, data, model=None):
        r"""
        Predict function for AutoML.

        Parameters
        ----------
        data :  DataFrame
            Data to be predicted.

            The first column of ``data`` must be the ID column.

        model : DataFrame, optional
            The model to be used for prediction.

            Defaults to the fitted model (model\_).

        Returns
        -------
        DataFrame
            Predicted result, structured as follows:

              - 1st column: Data type and name same as the 1st column of ``data``.
              - 2nd column: SCORE, predicted values(for regression) or class labels(for classification).
        """
        conn = data.connection_context
        if model is None:
            if getattr(self, 'model_', None) is None:
                msg = ('Model not initialized. Perform a fit first.')
                logger.error(msg)
                raise FitIncompleteError(msg)
            model = self.model_
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        outputs = ['RESULT', 'INFO']
        outputs = ['#PAL_AUTOML_{}_RESULT_TBL_{}_{}'.format(name, self.id, unique_id)
                   for name in outputs]
        result_tbl, info_tbl = outputs
        param_rows = []
        try:
            self._call_pal_auto(conn,
                                'PAL_PIPELINE_PREDICT',
                                data,
                                model,
                                ParameterTable().with_data(param_rows),
                                *outputs)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, outputs)
            self._status = -1
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, outputs)
            self._status = -1
            raise
        self._status = 1
        result_df = conn.table(result_tbl)
        self.predict_info_ = conn.table(info_tbl)
        return result_df

    def _operator_in_config(self, operator_name, config_dict):
        if operator_name in config_dict:
            return config_dict[operator_name]

    def evaluate(self,
                 data,
                 pipeline,
                 key=None,
                 features=None,
                 label=None,
                 categorical_variable=None,
                 resampling_method=None,
                 fold_num=None,
                 random_state=None):
        """
        This function is to evaluate the pipeline.

        Parameters
        ----------

        data : DataFrame

            Data for pipeline evaluation.

        pipeline : str or dict, optional
            Pipeline to be evaluated.

        key : str, optional

            Name of the ID column.

            Mandatory if ``data`` is not indexed, or the index of ``data`` contains multiple columns.

            Defaults to the single index column of ``data`` if not provided.

        features : list of str, optional

            Names of the feature columns.
            If ``features`` is not provided, it defaults to all non-ID,
            non-label columns.

        label : str, optional

            Name of the dependent variable.

            Defaults to the name of the last non-ID column.

        categorical_variable : str or list of str, optional
            Specify INTEGER column(s) that should be be treated as categorical
            data. Other INTEGER columns will be treated as continuous.

        resampling_method : {'cv', 'stratified_cv', 'bootstrap', 'stratified_bootstrap'}, optional
            The resampling method for model evaluation or parameter search.

            Once set, model evaluation or parameter search is enabled.

        fold_num : int, optional
            The fold number for cross validation.
            Valid only and mandatory when ``resampling_method`` is set
            as 'cv' or 'stratified_cv'.

        random_state : int, optional
            Specifies the seed for random number generator.

                - 0: Uses the current time (in seconds) as the seed.
                - Others: Uses the specified value as the seed.

        Returns
        -------

        DataFrame

            DataFrame of scores:

              - Score Name.
              - Score Value.
        """
        conn = data.connection_context
        require_pal_usable(conn)

        key = self._arg('key', key, str)
        index = data.index
        if isinstance(index, str):
            if key is not None and index != key:
                msg = "Discrepancy between the designated key column '{}' ".format(key) +\
                "and the designated index column '{}'.".format(index)
                logger.warning(msg)
        key = index if key is None else key
        features = self._arg('features', features, ListOfStrings)
        label = self._arg('label', label, str)
        if isinstance(categorical_variable, str):
            categorical_variable = [categorical_variable]
        categorical_variable = self._arg('categorical_variable', categorical_variable, ListOfStrings)
        cols = data.columns
        if key is not None:
            id_col = [key]
            cols.remove(key)
        else:
            id_col = []
        if label is None:
            label = cols[-1]
        cols.remove(label)
        if features is None:
            features = cols

        data_ = data[id_col + features + [label]]
        if isinstance(pipeline, dict):
            pipeline = json.dumps(pipeline)
        resampling_map = {'cv': 'cv', 'stratified_cv': 'stratified_cv', 'bootstrap': 'bootstrap',
                    'stratified_bootstrap': 'stratified_bootstrap'}
        resampling_method = self._arg('resampling_method', resampling_method, resampling_map)
        fold_num = self._arg('fold_num', fold_num, int)
        random_state = self._arg('random_state', random_state, int)
        param_rows = [
            ('HAS_ID', key is not None, None, None),
            ('RESAMPLING_METHOD', None, None, resampling_method),
            ('FOLD_NUM', fold_num, None, None),
            ('RANDOM_SEED', random_state, None, None),
            ('PIPELINE', None, None, pipeline)
            ]

        if categorical_variable is not None:
            param_rows.extend(('CATEGORICAL_VARIABLE', None, None, variable)
                              for variable in categorical_variable)
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        result_tbl = '#PAL_AUTOML_EVALUATED_RESULT_TBL_{}_{}'.format(self.id, unique_id)
        try:
            self._call_pal_auto(conn,
                                'PAL_PIPELINE_EVALUATE',
                                data_,
                                ParameterTable().with_data(param_rows),
                                result_tbl)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, result_tbl)
            raise
        except pyodbc.Error as db_err:
            logger.exception(str(db_err.args[1]))
            try_drop(conn, result_tbl)
            raise
        result_df = conn.table(result_tbl)
        return result_df

    def update_config_dict(self, operator_name, param_name=None, param_config=None):
        """
        Update the config dict.

        Parameters
        ----------
        operator_name : str
            The name of operator.

        param_name : str, optional
            The parameter name to be updated.
            If the parameter name doesn't exist in the config dict, it will create a new one.

            Defaults to None.
        param_config : any, optional
            The parameter config value.

            Defaults to None.
        """
        config_dict = json.loads(self.config_dict)
        get_operator_dict = self._operator_in_config(operator_name, config_dict)
        if get_operator_dict:
            config_dict[operator_name][param_name] = param_config
        else:
            if param_name:
                config_dict[operator_name] = {param_name: param_config}
            else:
                config_dict.update({operator_name: {}})
        self.config_dict = json.dumps(config_dict)

    def delete_config_dict(self, operator_name=None, category=None, param_name=None):
        """
        Delete the content of the config dict.

        Parameters
        ----------
        operator_name : str, optional
            It will delete the operator based on the given name in the config dict.

            Defaults to None.

        category : str, optional
            It will delete the whole given category in the config dict.

            Defaults to None.

        param_name : str, optional
            It will delete the parameter based on the given name once the operator name is provided.

            Defaults to None.
        """
        config_dict = json.loads(self.config_dict)
        result_dict = {}
        if category:
            for op_name in config_dict:
                if op_name in self._category_map:
                    if self._category_map[op_name] != category:
                        result_dict[op_name] = config_dict[op_name]
                else:
                    result_dict[op_name] = config_dict[op_name]
        else:
            for op_name in config_dict:
                if operator_name != op_name:
                    result_dict[op_name] = config_dict[op_name]
                elif param_name is not None:
                    operator_dict = config_dict[op_name]
                    operator_dict.pop(param_name)
                    result_dict[op_name] = operator_dict
        self.config_dict = json.dumps(result_dict)

    def display_config_dict(self, operator_name=None, category=None):
        """
        Display the config dict

        Parameters
        ----------
        operator_name : str, optional
            Only display the information on the given operator name.

            Defaults to None.

        category : str, optional
            Only display the information on the given category.

            Defaults to None.
        """
        if operator_name:
            print(operator_name)
            print(len(operator_name)  * "." + "\n")
            operator_dict = self._operator_in_config(operator_name, json.loads(self.config_dict))
            param = []
            config = []
            for key, value in operator_dict.items():
                param.append(key)
                config.append(value)
            print(pd.DataFrame({"Param": param, "Config": config}))
            print("\n")
        elif category:
            for op_name in json.loads(self.config_dict):
                if op_name in self._category_map:
                    if self._category_map[op_name] == category:
                        print(op_name)
                        print(len(op_name)  * "." + "\n")
                        param = []
                        config = []
                        operator_dict = self._operator_in_config(op_name, json.loads(self.config_dict))
                        for key, value in operator_dict.items():
                            param.append(key)
                            config.append(value)
                        print(pd.DataFrame({"Param": param, "Config": config}))
                        print("-" * 60 + "\n")
        else:
            category = []
            used_op = []
            for op_key in json.loads(self.config_dict):
                #op_key = list(operator_dict.keys())[0]
                used_op.append(op_key)
                if op_key in self._category_map:
                    category.append(self._category_map[op_key])
                else:
                    category.append('undefined')
            print(pd.DataFrame({"Used Operators": used_op, "Category": category}))
            print("\n" + "-" * 60 + "\n")
            for op_name in json.loads(self.config_dict):
                #op_name = list(operator_dict.keys())[0]
                print(op_name)
                print(len(op_name)  * "." + "\n")
                param = []
                config = []
                for key, value in json.loads(self.config_dict)[op_name].items():
                    param.append(key)
                    config.append(value)
                print(pd.DataFrame({"Param": param, "Config": config}))
                print("-" * 60 + "\n")

    def pipeline_plot(self, name="my_pipeline", iframe_height=450):
        """
        Pipeline plot.

        Parameters
        ----------
        name : str, optional
            The name of the pipeline plot.

            Defaults to 'my_pipeline'.

        iframe_height : int, optional
            The display height.

            Defaults to 450.
        """
        p_content = []
        p_args = []
        pipeline = json.loads(self.best_pipeline_.collect()["PIPELINE"].iat[0])
        pipe = _PipelineWalk(pipeline)
        for i in range(1, 100):
            p_content.append(pipe.current_content)
            p_args.append(pipe.current_args)
            pipe._next()
            if pipe.end:
                p_content.append(pipe.current_content)
                p_args.append(pipe.current_args)
                break
        p_content.reverse()
        p_args.reverse()
        count = 0
        nodes = []
        for p_1, p_2 in zip(p_content, p_args):
            nodes.append((str(p_1), str(p_2), [str(count)], [str(count + 1)]))
            count = count + 1
        digraph = Digraph(name)
        node = []
        for elem in nodes:
            node.append(digraph.add_python_node(elem[0],
                                                elem[1],
                                                in_ports=elem[2],
                                                out_ports=elem[3]))
        for node_x in range(0, len(node) - 1):
            digraph.add_edge(node[node_x].out_ports[0],
                             node[node_x + 1].in_ports[0])
        digraph.build()
        digraph.generate_notebook_iframe(iframe_height)

def _fetch_default_config_dict(connection_context, pipeline_type):
    unique_id = str(uuid.uuid1()).replace('-', '_').upper()
    outputs = ['#PAL_DEFAULT_CONFIG_DICT_{}_{}'.format(tbl, unique_id) for tbl in range(0, 2)]
    param_rows = []
    param_rows.extend([('PIPELINE_TYPE', None, None, pipeline_type)])
    param_rows.extend([('CONFIG_DICT', None, None, 'default')])
    try:
        PALBase()._call_pal_auto(connection_context,
                                 'PAL_AUTOML_CONFIG',
                                 ParameterTable().with_data(param_rows),
                                 *outputs)
    except dbapi.Error as db_err:
        logger.error(str(db_err))
        try_drop(connection_context, outputs)
        raise
    except pyodbc.Error as db_err:
        logger.error(str(db_err.args[1]))
        try_drop(connection_context, outputs)
        raise
    result = connection_context.table(outputs[0]).collect().iat[0, 1]
    try_drop(connection_context, outputs)
    return result

class AutomaticClassification(_AutoMLBase):
    """
    AutomaticClassification offers an intelligent search amongst machine learning pipelines for supervised classification tasks.
    Each machine learning pipeline contains several operators such as preprocessors, supervised classification models and transformer
    that follows API of hana-ml algorithms.

    Parameters
    ----------
    scorings : dict, optional
        AutomaticClassification supports multi-objective optimization with specified weights of each target.
        The goal is to maximize the target. Therefore,
        if you want to minimize the target, the target weight needs to be negative.

        The options are below:

        - AUC: Area Under Curve. The bigger, the better. Should use a positive weight.
        - ACCURACY: The percentage of samples that are correctly classified. The bigger, the better. Should use a positive weight.
        - KAPPA: Cohen's kappa. The bigger, the better. Should use a positive weight.
        - MCC: Matthews Correlation Coefficient. The bigger, the better. Should use a positive weight.
        - LAYERS: The number of operators. The smaller, the better. Should use a negative weight.
        - F1-SCORE (coming soon). The bigger, the better. Should use a positive weight.
        - PRECISION (coming soon). The bigger, the better. Should use a positive weight.
        - RECALL (coming soon). The bigger, the better. Should use a positive weight.

        Defaults to {"ACCURACY": 1.0, "AUC": 1.0}.

    generations : int, optional
        The number of iterations of pipeline optimization.

        Defaults to 5.

    populations_size : int, optional
        The number of indiviuals in each generation in genetic programming algorithm.

        Defaults to 20.

    offspring_size : int, optional
        The number of offsprings to produce in each generation.

        Defaults to 20.

    elite_number : int, optional
        The number of elite to produce in each generation.

        Defaults to 1/4*``population_size``.

    min_layer : int, optional
        The minimum number of operators in the pipeline.

        Defaults to 1.

    max_layer : int, optional
        The maximum number of operators in a pipeline.

        Defaults to 5.

    mutation_rate : float, optional
        The mutation rate for the genetic programming algorithm.

        Defaults to 0.9.

    crossover_rate : float, optional
        The crossover rate for the genetic programmming algorithm.

        Defaults to 0.1.

    random_seed : int, optional
        The seed for randomization.

        Defaults to the CPU time.

    config_dict : str, optional
        The customized configuration for the searching space.
        If it is None, the default config_dict will be used.

        Defaults to None.

    progress_indicator_id : str, optional
        It will be used in the progress monitor to visualize the progress of optimization.

        Defaults to None.

    fold_num : int, optional
        The number of fold in the cross validation process.

        Defaults to 5.

    resampling_method : {'cv', 'stratified_cv'}, optional
        The resampling method for cross validation process.
        The stratified cross validation is based on the label column.

        Defaults to 'stratified_cv'.

    max_eval_time_mins : float, optional
        The timeout setting for each operator. The unit is minute.

        Defaults to None.

    early_stop : int, optional
        The number of generations to check if there's no improvement in the optimization process.

        Defaults to 5.

    Attributes
    ----------
    best_pipeline_: DataFrame
        Best pipelines selected, structured as follows:

          - 1st column: ID, type INTEGER, pipeline IDs.
          - 2nd column: PIPELINE, type NVARCHAR, pipeline contents.
          - 3rd column: SCORES, type NVARCHAR, scoring metrics for pipeline.

        Avaliable only when the ``pipeline`` parameter is not specified during the fitting process.

    model_ : DataFrame
        Fitted AutomaticClassification pipeline model, structured as follows:

          - 1st column: ROW_INDEX
          - 2nd column: MODEL_CONTENT

    info_ : DataFrame
        Related info/statistics for AutomaticClassification pipeline fitting, structured as follows:

          - 1st column: STAT_NAME
          - 2nd column: STAT_VALUE

    Examples
    --------

    Create an AutomaticClassification instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_c = AutomaticClassification(generations=2,
                                         population_size=5,
                                         offspring_size=5,
                                         progress_indicator_id=progress_id)
    >>> auto_c.enable_workload_class("MY_WORKLOAD_CLASS")

    Invoke a PipelineProgressStatusMonitor:

    >>> progress_status_monitor = PipelineProgressStatusMonitor(connection_context=dataframe.ConnectionContext(url, port, user, pwd),
                                                                automatic_obj=auto_c)
    >>> progress_status_monitor.start()
    >>> auto_c.fit(data=df_train)

    Output:

    .. image:: progress_classification.png

    Show the best pipeline:

    >>> print(auto_c.best_pipeline_.collect())
    ID                                           PIPELINE  \
     0  {"HGBT_Classifier":{"args":{"ITER_NUM":100,"MA...
                                               SCORES
    {"ACCURACY":0.6726642676262828,"AUC":0.7516449...

    Plot the best pipeline:

    >>> BestPipelineReport(auto_c).generate_notebook_iframe()

    .. image:: best_pipeline_classification.PNG

    Make prediction:

    >>> res = auto_c.predict(df_test)
    >>> print(res.collect())
     ID SCORES
    702      1
    502      0
    ...    ...
    103      0
    208      0
    140      0
    282      1
    581      0

    If you want to use an existing pipeline to fit and predict:

    >>> pipeline = auto_c.best_pipeline_.collect().iat[0, 1]
    >>> auto_c.fit(df_train, pipeline=pipeline)
    >>> res = auto_c.predict(df_test)

    """
    def __init__(self,
                 scorings=None,
                 generations=None,
                 population_size=None,
                 offspring_size=None,
                 elite_number=None,
                 min_layer=None,
                 max_layer=None,
                 mutation_rate=None,
                 crossover_rate=None,
                 random_seed=None,
                 config_dict=None,
                 progress_indicator_id=None,
                 fold_num=None,
                 resampling_method=None,
                 max_eval_time_mins=None,
                 early_stop=None):
        super(AutomaticClassification, self).__init__(scorings,
                                                      generations,
                                                      population_size,
                                                      offspring_size,
                                                      elite_number,
                                                      min_layer,
                                                      max_layer,
                                                      mutation_rate,
                                                      crossover_rate,
                                                      random_seed,
                                                      config_dict,
                                                      progress_indicator_id,
                                                      fold_num,
                                                      resampling_method,
                                                      max_eval_time_mins,
                                                      early_stop)
        if self.config_dict is None:
            config_dict_file = os.path.join(os.path.dirname(__file__), "templates",
                                            "config_dict_classification_default.json")
            with open(config_dict_file) as input_file:
                self.config_dict = json.dumps(json.load(input_file))

    def _get_highlight_metric(self):
        if self.scorings:
            return list(json.loads(self.scorings).keys())[0]
        return 'AUC'

    def reset_config_dict(self, connection_context=None):
        """
        Reset the config dict.

        Parameters
        ----------
        connection_context : ConnectionContext, optional
            If it is set, the default config dict will use the one stored in SAP HANA.
        """
        if connection_context:
            self.config_dict = _fetch_default_config_dict(connection_context, 'classifier')
        else:
            config_dict_file = os.path.join(os.path.dirname(__file__), "templates",
                                            "config_dict_classification_default.json")
            with open(config_dict_file) as input_file:
                self.config_dict = json.dumps(json.load(input_file))

class AutomaticRegression(_AutoMLBase):
    """

    AutomaticRegression offers an intelligent search amongst machine learning pipelines for supervised regression tasks.
    Each machine learning pipeline contains several operators such as preprocessors, supervised regression models and transformer
    that follows API of hana-ml algorithms.

    Parameters
    ----------
    scorings : dict, optional
        AutomaticRegression supports multi-objective optimization with specified weights of each target.
        The goal is to maximize the target. Therefore,
        if you want to minimize the target, the weight of target needs to be negative.

        The target options are below:

        - R2: R-squared. The bigger, the better. Should use a positive weight.
        - RMSE: Root Mean Squared Error. The smaller, the better. Should use a negative weight.
        - MAE: Mean Absolute Error. The smaller, the better. Should use a negative weight.
        - WMAPE: Weighted Mean Absolute Percentage Error. The smaller, the better. Should use a negative weight.
        - MSLE: Mean Squared Logarithmic Error. The smaller, the better. Should use a negative weight.
        - MAX_ERROR: The max absolute difference between the observed value and the expected value. The smaller, the better. Should use a negative weight.
        - EVAR: Explained Variance measures the proportion to which a mathematical model accounts for the variation (dispersion) of a given data set. The bigger, the better. Should use a positive weight.
        - LAYERS: The number of operators. The smaller, the better. Should use a negative weight.

        Defaults to {MAE":-1.0, "EVAR":1.0}.

    generations : int, optional
        The number of iterations of the pipeline optimization.

        Defaults to 5.

    populations_size : int, optional
        The number of indiviuals in each generation in genetic programming algorithm.

        Defaults to 20.

    offspring_size : int, optional
        The number of offsprings to produce in each generation.

        Defaults to 20.

    elite_number : int, optional
        The number of elite to produce in each generation.

        Defaults to 1/4*population_size.

    min_layer : int, optional
        The minimum number of operators in the pipeline.

        Defaults to 1.

    max_layer : int, optional
        The maximum number of operators in the pipeline.

        Defaults to 5.

    mutation_rate : float, optional
        The mutation rate for the genetic programming algorithm.

        Defaults to 0.9.

    crossover_rate : float, optional
        The crossover rate for the genetic programmming algorithm.

        Defaults to 0.1.

    random_seed : int, optional
        The seed for randomization.

        Defaults to the CPU time.

    config_dict : str, optional
        The customized configuration for the searching space.
        If it is None, the default config_dict will be used.

        Defaults to None.

    progress_indicator_id : str, optional
        It will be used in the progress monitor to visualize the progress of optimization.

        Defaults to None.

    fold_num : int, optional
        The number of fold in the cross validation process.

        Defaults to 5.

    resampling_method : {'cv'}, optional
        The resampling method for cross validation process.

        Defaults to 'cv'.

    max_eval_time_mins : float, optional
        The timeout setting for each operator. The unit is minute.

        Defaults to None.

    early_stop : int, optional
        The number of generations to check if there's no improvement in the optimization process.

        Defaults to 5.

    Attributes
    ----------
    best_pipeline_: DataFrame
        Best pipelines selected, structured as follows:

          - 1st column: ID, type INTEGER, pipeline IDs.
          - 2nd column: PIPELINE, type NVARCHAR, pipeline contents.
          - 3rd column: SCORES, type NVARCHAR, scoring metrics for pipeline.

        Avaliable only when the ``pipeline`` parameter is not specified during the fitting process.

    model_ : DataFrame
        Fitted AutomaticClassification pipeline model, structured as follows:

          - 1st column: ROW_INDEX
          - 2nd column: MODEL_CONTENT

    info_ : DataFrame
        Related info/statistics for AutomaticClassification pipeline fitting, structured as follows:

          - 1st column: STAT_NAME
          - 2nd column: STAT_VALUE

    Examples
    --------

    Create an AutomaticRegression instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_r = AutomaticRegression(generations=5,
                                     population_size=5,
                                     offspring_size=5,
                                     scorings={'MSE':1.0, 'LAYERS':0.05},
                                     progress_indicator_id=progress_id)
    >>> auto_r.enable_workload_class("MY_WORKLOAD_CLASS")

    Invoke a PipelineProgressStatusMonitor:

    >>> progress_status_monitor = PipelineProgressStatusMonitor(connection_context=dataframe.ConnectionContext(url, port, user, pwd),
                                                                automatic_obj=auto_c)
    >>> progress_status_monitor.start()
    >>> auto_r.fit(data=df_train)

    Show the best pipeline:

    >>> print(auto_c.best_pipeline_.collect())

    Plot the best pipeline:

    >>> BestPipelineReport(auto_r).generate_notebook_iframe()

    Make prediction:

    >>> res = auto_r.predict(df_test)

    If you want to use an existing pipeline to fit and predict:

    >>> pipeline = auto_r.best_pipeline_.collect().iat[0, 1]
    >>> auto_r.fit(df_train, pipeline=pipeline)
    >>> res = auto_r.predict(df_test)
    """
    def __init__(self,
                 scorings=None,
                 generations=None,
                 population_size=None,
                 offspring_size=None,
                 elite_number=None,
                 min_layer=None,
                 max_layer=None,
                 mutation_rate=None,
                 crossover_rate=None,
                 random_seed=None,
                 config_dict=None,
                 progress_indicator_id=None,
                 fold_num=None,
                 resampling_method='cv',
                 max_eval_time_mins=None,
                 early_stop=None):
        super(AutomaticRegression, self).__init__(scorings,
                                                  generations,
                                                  population_size,
                                                  offspring_size,
                                                  elite_number,
                                                  min_layer,
                                                  max_layer,
                                                  mutation_rate,
                                                  crossover_rate,
                                                  random_seed,
                                                  config_dict,
                                                  progress_indicator_id,
                                                  fold_num,
                                                  resampling_method,
                                                  max_eval_time_mins,
                                                  early_stop)
        if self.config_dict is None:
            config_dict_file = os.path.join(os.path.dirname(__file__), "templates",
                                            "config_dict_regression_default.json")
            with open(config_dict_file) as input_file:
                self.config_dict = json.dumps(json.load(input_file))

    def _get_highlight_metric(self):
        if self.scorings:
            return list(json.loads(self.scorings).keys())[0]
        return 'MAE'

    def reset_config_dict(self, connection_context=None):
        """
        Reset config dict.

        Parameters
        ----------
        connection_context : ConnectionContext, optional
            If it is set, the default config dict will use the one stored in HANA DB.

            Defaults to None.
        """
        if connection_context:
            self.config_dict = _fetch_default_config_dict(connection_context, 'regressor')
        else:
            config_dict_file = os.path.join(os.path.dirname(__file__), "templates",
                                            "config_dict_regression_default.json")
            with open(config_dict_file) as input_file:
                self.config_dict = json.dumps(json.load(input_file))


class _PipelineWalk:

    def __init__(self, pipeline):
        self.current_walk = pipeline
        self.end = False
        if isinstance(self.current_walk, dict):
            self.current_content = list(self.current_walk.keys())[0]
            self.current_args = list(self.current_walk.values())[0]['args']
        else:
            self.current_content = self.current_walk
            self.current_args = ''
            self.end = True

    def _next(self):
        if 'inputs' in self.current_walk[self.current_content]:
            if 'data' in self.current_walk[self.current_content]['inputs']:
                self.current_walk = self.current_walk[self.current_content]['inputs']['data']
                if isinstance(self.current_walk, dict):
                    self.current_content = list(self.current_walk.keys())[0]
                    self.current_args = list(self.current_walk.values())[0]['args']
                else:
                    self.current_content = self.current_walk
                    self.current_args = ''
                    self.end = True

class Preprocessing(PALBase):
    """
    Preprocessing class. Similar to the function preprocessing.

    Parameters
    ----------
    name : str
        The preprocessing algorithm name.

        - OneHotEncoder.
        - FeatureNormalizer.
        - KBinsDiscretizer.
        - Imputer.
        - Discretize.
        - MDS.
        - SMOTE.
        - SMOTETomek.
        - TomekLinks.
        - Sampling.

    **kwargs: dict
        A dict of the keyword args passed to the object.
        Please refer to the documentation of the specific preprocessing for parameter information.
    """
    def __init__(self, name, **kwargs):
        super(Preprocessing, self).__init__()
        self.name = name
        self.kwargs = dict(**kwargs)

    def fit_transform(self, data, key=None, features=None, **kwargs):
        """
        Execute the preprocessing algorithm and return the transformed dataset.

        Parameters
        ----------
        data : DataFrame
            Input data.

        key : str, optional
            Name of the ID column.

            Defaults to the index column of ``data`` (i.e. data.index) if it is set.

        features : list, optional
            The columns to be preprocessed.

            Defaults to None.

        **kwargs: dict
            A dict of the keyword args passed to the fit_transform function.
            Please refer to the documentation of the specific preprocessing for parameter information.
        """
        args = dict(**kwargs)
        if data.index is not None:
            key = data.index
        key_is_none = False
        if key is None:
            key_is_none = True
        if features is None:
            features = data.columns
            if self.name == 'OneHotEncoder':
                features = []
                for col, val in data.get_table_structure().items():
                    if 'VARCHAR' in val.upper():
                        features.append(col)
            if key is not None:
                if key in features:
                    features.remove(key)
        if isinstance(features, str):
            features = [features]
        if self.name != "OneHotEncoder":
            if key is None:
                key = "ID"
                data = data.add_id(key)
            data = data.select([key] + features)
        other = data.deselect(features)
        if self.name == 'FeatureNormalizer':
            if 'method' not in self.kwargs.keys():
                self.kwargs['method'] = "min-max"
                self.kwargs['new_max'] = 1.0
                self.kwargs['new_min'] = 0.0
            transformer = FeatureNormalizer(**self.kwargs)
            result = transformer.fit_transform(data, key, **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'KBinsDiscretizer':
            if 'strategy' not in self.kwargs.keys():
                self.kwargs['strategy'] = "uniform_size"
                self.kwargs['smoothing'] = "means"
            transformer = KBinsDiscretizer(**self.kwargs)
            result = transformer.fit_transform(data, key, **args).deselect(["BIN_INDEX"])
            self.execute_statement = transformer.execute_statement
        elif self.name == 'Imputer':
            transformer = Imputer(**self.kwargs)
            result = transformer.fit_transform(data,
                                               key,
                                               **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'Discretize':
            if 'strategy' not in self.kwargs.keys():
                self.kwargs['strategy'] = "uniform_size"
                self.kwargs['smoothing'] = "bin_means"
            transformer = Discretize(**self.kwargs)
            if 'binning_variable' not in args.keys():
                args['binning_variable'] = features
            result = transformer.fit_transform(data,
                                               **args)[0]
            self.execute_statement = transformer.execute_statement
        elif self.name == 'MDS':
            if 'matrix_type' not in self.kwargs.keys():
                self.kwargs['matrix_type'] = "observation_feature"
            transformer = MDS(**self.kwargs)
            result = transformer.fit_transform(data, key, **args)
            result = result[0].pivot_table(values='VALUE', index='ID', columns='DIMENSION', aggfunc='avg')
            columns = result.columns
            rename_cols = {}
            for col in columns:
                if col != "ID":
                    rename_cols[col] = "X_" + str(col)
            result = result.rename_columns(rename_cols)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'SMOTE':
            transformer = SMOTE(**self.kwargs)
            result = transformer.fit_transform(data, **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'SMOTETomek':
            transformer = SMOTETomek(**self.kwargs)
            result = transformer.fit_transform(data,
                                               **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'TomekLinks':
            transformer = TomekLinks(**self.kwargs)
            result = transformer.fit_transform(data,
                                               key=key,
                                               **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'Sampling':
            transformer = Sampling(**self.kwargs)
            result = transformer.fit_transform(data, **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'PCA':
            transformer = PCA(**self.kwargs)
            result = transformer.fit_transform(data,
                                               key=key,
                                               **args)
            self.execute_statement = transformer.execute_statement
        elif self.name == 'OneHotEncoder':
            others = list(set(data.columns) - set(features))
            query = "SELECT {}".format(", ".join(others))
            if others:
                query = query + ", "
            for feature in features:
                categoricals = data.distinct(feature).collect()[feature].to_list()
                for cat in categoricals:
                    query = query + "CASE WHEN \"{0}\" = '{1}' THEN 1 ELSE 0 END \"{1}_{0}_OneHot\", ".format(feature, cat)
            query = query[:-2] + " FROM ({})".format(data.select_statement)
            self.execute_statement = query
            return data.connection_context.sql(query)
        elif self.name == 'FeatureSelection':
            transformer = FeatureSelection(**self.kwargs)
            result = transformer.fit_transform(data,
                                               key,
                                               **args)
            self.execute_statement = transformer.execute_statement
        else:
            pass
        if features is not None:
            if key is not None:
                result = other.set_index(key).join(result.set_index(key))
        if key_is_none:
            result = result.deselect(key)
        return result
