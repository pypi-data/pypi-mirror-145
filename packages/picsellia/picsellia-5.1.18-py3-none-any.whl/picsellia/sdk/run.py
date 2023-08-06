import json
import logging
from typing import List

from beartype import beartype
from picsellia.decorators import exception_handler
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
import subprocess

from picsellia.sdk.experiment import Experiment
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia.types.schemas import RunSchema
logger = logging.getLogger('picsellia')


class Run(Dao):

    def __init__(self, connexion: Connexion, data: dict) -> None:
        run = RunSchema(**data)
        super().__init__(connexion, run.id)
        self._config = run.config
        self._script = run.script
        self._script_object_name = run.script_object_name
        self._requirements = run.requirements

    @property
    def config(self) -> dict:
        return self._config

    @property
    def requirements(self) -> List[dict]:
        return self._requirements

    @property
    def script(self) -> str:
        assert self._script != None, "Script is not defined yet"
        return self._script

    @property
    def script_object_name(self) -> str:
        assert self._script != None and self._script_object_name != None, "Script is not defined yet"
        return self._script_object_name

    def __str__(self,): return "{}Run{} (id: {})".format(bcolors.BLUE, bcolors.ENDC, self.id)

    @exception_handler
    @beartype
    def update(self, **kwargs) -> None:
        """Update this run with the given keyword arguments.

        Examples:
            ```python
                run.update(status="running")
            ```
        """
        data = json.dumps(kwargs)
        self.connexion.patch('/sdk/v1/run/{}'.format(self.id), data=data)

    @exception_handler
    @beartype
    def end(self,) -> None:
        """End a run

        Examples:
            ```python
                run.end()
            ```
        """
        self.connexion.post('/sdk/v1/run/{}/end'.format(self.id))

    @exception_handler
    @beartype
    def download_script(self,) -> str:
        """Locally download the script from the run.

        Returns:
            Filename of the script locally downloaded
        """
        assert self.script is not None, "Run script is not yet defined"

        if self.connexion.download_some_file(False, self.script_object_name, self.script):
            logger.info('{} downloaded successfully'.format(self.script))
        else:
            logger.error("Could not download {} file".format(self.script))
        return self.script

    @exception_handler
    @beartype
    def download_data(self,) -> List[str]:
        """Download run data from the run.

        Examples:
            ```python
                run.download_data()
            ```

        Returns:
            Filenames of the data locally downloaded
        """
        assert "data" in self.config.keys(), "Run configuration is not yet defined"

        data_list = self.config["data"]
        filenames = []
        for data in data_list:
            filename = data["filename"]
            if self.connexion.download_some_file(False, data["object_name"], filename):
                filenames.append(filename)
        
        logger.info('{} downloaded successfully'.format(filenames))
        return filenames

    @exception_handler
    @beartype
    def install_requirements(self,) -> None:
        """Install requirements from the run requirements dictionnary.

        Examples:
            ```python
                run.install_requirements()
            ```
        """
        assert self.id is not None, "Please get a run first."
        req = self.requirements
        for module in req:
            name = "{}=={}".format(
                module["package"], module["version"]) if module["version"] != "" else module["package"]
            subprocess.call(['pip', 'install', name])

    @exception_handler
    @beartype
    def get_experiment(self, ) -> Experiment:
        """Retrieve linked experiment

        Examples:
            ```python
                my_experiment = run.get_experiment()
            ```

        Returns:
            An (Experiment) object linked to this run
        """
        r = self.connexion.get('/sdk/v1/run/{}/experiment'.format(self.id)).json()
        return Experiment(self.connexion, r["experiment"])

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete this run from the platform.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
                run.delete()
            ```
        """
        self.connexion.delete('/sdk/v1/run/{}'.format(self.id))
        logger.info("Run (id: {}) deleted from platform.".format(self.id))

