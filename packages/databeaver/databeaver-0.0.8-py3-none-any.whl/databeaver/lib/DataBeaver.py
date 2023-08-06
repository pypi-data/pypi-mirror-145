import re
import shutil
import tomli
import os.path
import logging
import multiprocessing
from .constants import ConfigFormats
from .NotInstantiatedError import NotInstantiatedError
from .DataModel import DataModel
import signal
import yaml

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

class DataBeaver:
    """
    Responsible For
    - Data Model Orchestration (the building of 1 or more data models)
    """
    LOGGER = "databeaver"

    def __init__(self, config_file=None, config_format=None):
        """

        :param config_file: Name of the configuration file to be used
        :param config_format: Optional command line arguments (used when DataBeaver is invoked via the command line)

        """
        # Variable initialization
        _configFile = None
        _configFormat = None

        logging.basicConfig(level=logging.INFO)

        # PRODUCTION - Com
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(self.LOGGER).addHandler(logging.NullHandler())

        self.logger = logging.getLogger(self.LOGGER)

        self.instantiated = False
        if config_file:
            with open(config_file, "rb") as f:
                self.config = tomli.load(f)
                self.logger.info(self.config)
                self.instantiated = self._config_is_valid()

    def _config_is_valid(self):
        """
        Responsible for making sure the configuration provided is actually, specifically
        1. Number of Processes to use has been specified
        2. At least one data model has been specified

        :return:
        """
        # {'CONFIG': {'PROCESSES': 4, 'DATA_MODELS': ['model1', 'model2']}, 'TARGET': [
        #     {'TYPE': 'POSTGRES', 'ENVIRONMENT': 'DEVELOPMENT', 'HOST': 'localhost',
        #      'DATABASE': 'development__fbb__sports_betting', 'USER': 'sports_betting',
        #      'PASSWORD': 'ENV:DATABASE_PASSWORD'}], 'model1': {'FILE_LOCATION': '/path/to/model/files'},
        #  'model2': {'FILE_LOCATION': '/path/to/model/files'}}

        # Check if Number of Processes to use has been specified
        if 'PROCESSES' not in self.config:
            return False

        # Check if
        if 'DATA_MODELS' not in self.config or not isinstance(self.config['DATA_MODEL'], list):
            return False

        for model_name in self.config['DATA_MODEL']:
            if model_name not in self.config:
                return False

            if 'FILES' not in self.config[model_name] or not os.path.isdir(self.config[model_name]['FILES']):
                return False

        return True

    def build(self):
        """
        Responsible For:
        Generating the tables for this model in the specified destination
        :return:
        """
        if not self.instantiated:
            msg = f"No configuration provided."
            raise NotInstantiatedError(message=msg)

        # Check the project file exists and
        # Read YAML file
        with open(self.args.project_file, 'r') as stream:
            yaml_config = yaml.safe_load(stream)

        # Look for models in the directories specified in the project file
        model_files = []
        for directory in yaml_config['model-locations']:
            files = [f"{directory}/{file}" for file in os.listdir(directory)]
            model_files.extend(files)

        # Determine model dependencies to eventually establish execution order
        logger = self.get_logger()

        # Iterate over all the models and generate the compiled sql that we will run against the database
        # We will also generate the model dependencies
        model_info = {}
        file_info = {}
        for model_file_name in model_files:
            model_name = model_file_name[model_file_name.rfind('/') + 1:model_file_name.find('.')]

            # Check if this is the first time we have seen this model
            if model_name not in model_info:
                model_info[model_name] = {'steps': [], 'current_step': 0, 'status': self.MODEL_NOT_BUILT}

            if model_file_name not in file_info:
                file_info[model_file_name] = {'dependencies': [], 'status': self.EXECUTION_NOT_EXECUTED}

            # Add this model to the steps for the table
            model_info[model_name]['steps'].append(model_file_name)

            # Add any dependency based on having prior steps in the model to run
            if model_file_name.count('.') == 3:
                # Get the index number
                start_pos = model_file_name.find('.') + 1
                end_pos = model_file_name.find('.', start_pos, len(model_file_name))
                index_number = int(model_file_name[start_pos:end_pos])

                if index_number > 1:
                    previous_sql_name = model_file_name.replace(f'.{index_number}.', f'.{index_number - 1}.')
                    file_info[model_file_name]['dependencies'].append(previous_sql_name)
            else:
                logger.error(f"{model_file_name} can not be parsed and will be ignored.")
                continue

            # Load the sql out of the file
            with open(model_file_name, 'r') as model_file:
                raw_sql = model_file.read()
            file_info[model_file_name]['raw_sql'] = raw_sql

        file_info = self._parse_sql(model_info, file_info)

        processes = yaml_config['processes']
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        with multiprocessing.Pool(processes) as pool:
            signal.signal(signal.SIGINT, original_sigint_handler)

            # Loop over the models we will create until no more work can be done
            continue_processing = True
            loop_counter = 1

            while continue_processing:
                logger.info(f"Pass #{loop_counter}")
                loop_counter += 1

                # Determine all files we want to process in this pass
                files_to_process = []
                continue_processing = False
                for model_name in model_info.keys():
                    # Only process MODEL_NOT_BUILT models
                    if model_info[model_name]['status'] != self.MODEL_NOT_BUILT:
                        continue

                    # Get the file we will process for this model in this pass
                    current_step = model_info[model_name]['current_step']
                    # print(f"{current_step} = {model_name}.current_step")
                    filename_to_execute = model_info[model_name]['steps'][current_step]

                    # If all the dependencies have been satisfied, add the file to the list of files to be processed
                    if len(file_info[filename_to_execute]['dependencies']) == 0:
                        logger.info(f"{model_name} : {filename_to_execute} will be executed.")
                        files_to_process.append((filename_to_execute, file_info[filename_to_execute]['sql']))

                # print(files_to_process)

                # Execute all the sql statements for this pass in parallel
                results = pool.imap_unordered(process_file, files_to_process)

                # Update file dependencies and model build status based on the results returned
                for (filename_executed, execution_status, db_error) in results:
                    executed_model_name = filename_executed[
                                          filename_executed.find('/') + 1:filename_executed.find('.')]

                    # This file successfully executed and can be removed from any dependencies
                    if self.EXECUTION_SUCCEEDED == execution_status:
                        continue_processing = True
                        logger.info(f"{filename_executed} - {execution_status}")
                        model_info[executed_model_name]['current_step'] = current_step + 1
                        # print(f"{model_name}.current_step = {model_info[model_name]['current_step']}")

                        for file_name, file in file_info.items():
                            if filename_executed in file['dependencies']:
                                file_info[file_name]['dependencies'].remove(filename_executed)

                    elif self.EXECUTION_FAILED == execution_status:
                        logger.info(f"{model_name} - {self.MODEL_FAILED}")
                        model_info[executed_model_name]['status'] = self.MODEL_FAILED

                    # If we executed the last file in steps the model is built
                    if model_info[executed_model_name]['current_step'] == len(model_info[model_name]['steps']):
                        model_info[executed_model_name]['status'] = self.MODEL_BUILT
                        query_params = {'table': executed_model_name}
                        results = self.execute_sql('select_table_count.tmpl.sql', query_params)
                        logger.info(
                            f"{executed_model_name} - {self.MODEL_BUILT} - {results[0]['count']} rows loaded")

                    return
                    if loop_counter > 3:
                        return

        #
        # models_to_execute = self.config['DATA_MODELS']
        # for model_name in models_to_execute:
        #     data_model = DataModel(self.config)
        #     data_model.build()

    def create_project(self, name, config_format=ConfigFormats.TOML):
        """
        Create a new empty
        :return:
        """
        print(self.logger)
        self.logger.info('Creating new project')

        # self.logger.info('Creating new data modelling project')
        # Get the project name from the user and generate the directory name we will use
        directory_name = re.sub(' ', '_', name)
        directory_name = re.sub('[^A-Za-z0-9_]+', '', directory_name)
        self.logger.info(f"Project name is '{name}'")

        # Check if the directory already exists
        if os.path.isdir(directory_name):
            self.logger.error(f"{directory_name} already exists, operation can not be completed.")
            return

        # Make the top level project directory
        os.mkdir(directory_name)
        self.logger.info(f'Created {directory_name}')

        # Make the directory for configuration files
        config_directory = f"{directory_name}/system"
        os.mkdir(config_directory)
        self.logger.info(f'Created {config_directory}')

        # Get the data for the sample config file and set the file name for the sample config file
        config_sample = ''
        if config_format is ConfigFormats.TOML:
            file_name = "databeaver.toml"
            config_sample = pkg_resources.read_text('databeaver.data', 'configSample.toml')
        elif config_format is ConfigFormats.YAML:
            file_name = "databeaver.yaml"
        elif config_format is ConfigFormats.INI:
            file_name = "databeaver.ini"
            config_sample = pkg_resources.read_text('databeaver.data', 'configSample.ini')
        elif config_format is ConfigFormats.JSON:
            file_name = "databeaver.json"

        # Write the config file to the file system
        file_path = f"{config_directory}/{file_name}"
        with open(file_path) as f:
            f.write(config_sample)

    def init_from_file(self, config_file):
        """
        Add configuration post class instantiation

        :param config_file: Path to the TOML configuration file to use
        :return:
        """
        with open(config_file, "rb") as f:
            self.config = tomli.load(f)
            self.instantiated = self._config_is_valid()
        #
        # # Look for models in the directories specified in the project file
        # model_files = []
        # for directory in yaml_config['model-locations']:
        #     files = [f"{directory}/{file}" for file in os.listdir(directory)]
        #     model_files.extend(files)
        #
        # # Determine model dependencies to eventually establish execution order
        # logger = self.get_logger()
        #
        # # Iterate over all the models and generate the compiled sql that we will run against the database
        # # We will also generate the model dependencies
        # model_info = {}
        # file_info = {}
        # for model_file_name in model_files:
        #     model_name = model_file_name[model_file_name.rfind('/') + 1:model_file_name.find('.')]
        #
        #     # Check if this is the first time we have seen this model
        #     if model_name not in model_info:
        #         model_info[model_name] = {'steps': [], 'current_step': 0, 'status': self.MODEL_NOT_BUILT}
        #
        #     if model_file_name not in file_info:
        #         file_info[model_file_name] = {'dependencies': [], 'status': self.EXECUTION_NOT_EXECUTED}
        #
        #     # Add this model to the steps for the table
        #     model_info[model_name]['steps'].append(model_file_name)
        #
        #     # Add any dependency based on having prior steps in the model to run
        #     if model_file_name.count('.') == 3:
        #         # Get the index number
        #         start_pos = model_file_name.find('.')+1
        #         end_pos = model_file_name.find('.', start_pos, len(model_file_name))
        #         index_number = int(model_file_name[start_pos:end_pos])
        #
        #         if index_number > 1:
        #             previous_sql_name = model_file_name.replace(f'.{index_number}.', f'.{index_number-1}.')
        #             file_info[model_file_name]['dependencies'].append(previous_sql_name)
        #     else:
        #         logger.error(f"{model_file_name} can not be parsed and will be ignored.")
        #         continue
        #
        #     # Load the sql out of the file
        #     with open(model_file_name, 'r') as model_file:
        #         raw_sql = model_file.read()
        #     file_info[model_file_name]['raw_sql'] = raw_sql
        #
        # file_info = self._parse_sql(model_info, file_info)
        #
        # processes = yaml_config['processes']
        # original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        # with multiprocessing.Pool(processes) as pool:
        #     signal.signal(signal.SIGINT, original_sigint_handler)
        #
        #     # Loop over the models we will create until no more work can be done
        #     continue_processing = True
        #     loop_counter = 1
        #
        #     while continue_processing:
        #         logger.info(f"Pass #{loop_counter}")
        #         loop_counter += 1
        #
        #         # Determine all files we want to process in this pass
        #         files_to_process = []
        #         continue_processing = False
        #         for model_name in model_info.keys():
        #             # Only process MODEL_NOT_BUILT models
        #             if model_info[model_name]['status'] != self.MODEL_NOT_BUILT:
        #                 continue
        #
        #             # Get the file we will process for this model in this pass
        #             current_step = model_info[model_name]['current_step']
        #             # print(f"{current_step} = {model_name}.current_step")
        #             filename_to_execute = model_info[model_name]['steps'][current_step]
        #
        #             # If all the dependencies have been satisfied, add the file to the list of files to be processed
        #             if len(file_info[filename_to_execute]['dependencies']) == 0:
        #                 logger.info(f"{model_name} : {filename_to_execute} will be executed.")
        #                 files_to_process.append((filename_to_execute, file_info[filename_to_execute]['sql']))
        #
        #         # print(files_to_process)
        #
        #         # Execute all the sql statements for this pass in parallel
        #         results = pool.imap_unordered(process_file, files_to_process)
        #
        #         # Update file dependencies and model build status based on the results returned
        #         for (filename_executed, execution_status, db_error) in results:
        #             executed_model_name = filename_executed[filename_executed.find('/')+1:filename_executed.find('.')]
        #
        #             # This file successfully executed and can be removed from any dependencies
        #             if self.EXECUTION_SUCCEEDED == execution_status:
        #                 continue_processing = True
        #                 logger.info(f"{filename_executed} - {execution_status}")
        #                 model_info[executed_model_name]['current_step'] = current_step + 1
        #                 # print(f"{model_name}.current_step = {model_info[model_name]['current_step']}")
        #
        #                 for file_name, file in file_info.items():
        #                     if filename_executed in file['dependencies']:
        #                         file_info[file_name]['dependencies'].remove(filename_executed)
        #
        #             elif self.EXECUTION_FAILED == execution_status:
        #                 logger.info(f"{model_name} - {self.MODEL_FAILED}")
        #                 model_info[executed_model_name]['status'] = self.MODEL_FAILED
        #
        #             # If we executed the last file in steps the model is built
        #             if model_info[executed_model_name]['current_step'] == len(model_info[model_name]['steps']):
        #                 model_info[executed_model_name]['status'] = self.MODEL_BUILT
        #                 query_params = {'table': executed_model_name}
        #                 results = self.execute_sql('select_table_count.tmpl.sql', query_params)
        #                 logger.info(f"{executed_model_name} - {self.MODEL_BUILT} - {results[0]['count']} rows loaded")
        #
        #             return
        #             if loop_counter > 3:
        #                 return
