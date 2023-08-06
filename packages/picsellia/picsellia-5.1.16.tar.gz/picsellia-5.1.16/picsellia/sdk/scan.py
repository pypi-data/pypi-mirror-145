import logging
from beartype import beartype
from picsellia.decorators import exception_handler
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
from picsellia.sdk.run import Run
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia.types.schemas import ScanSchema

logger = logging.getLogger('picsellia')

class Scan(Dao):

    def __init__(self, connexion: Connexion, data: dict) -> None:
        scan = ScanSchema(**data)
        super().__init__(connexion, scan.id)
        self._name = scan.name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self,): return "{}Scan '{}' {} (id: {})".format(bcolors.BLUE, self.name, bcolors.ENDC, self.id)

    @exception_handler
    @beartype
    def launch(self,) -> None:
        """Distribute runs remotely for this scan.

        :information-source: The remote environment has to be setup prior launching the experiment.
        It defaults to our remote training engine.

        Examples:
            ```python
                scan.launch()
            ```
        """
        self.connexion.post('/sdk/v1/scan/{}/launch'.format(self.id))

    @exception_handler
    @beartype
    def get_run_by_id(self, id: str) -> Run:
        """Retrieve a run object by its id.

        Examples:
            ```python
                scan.get_run_by_id("cb750009-4e09-42bb-8c84-cc78aa004bf0")
            ```
        Arguments:
            id (str): id (primary key) of the run on Picsellia

        Returns:
            A (Run) object manipulable
        """
        r = self.connexion.get('/sdk/v1/run/{}'.format(id)).json()
        return Run(self.connexion, r["run"])

    @exception_handler
    @beartype
    def get_next_run(self,) -> Run:
        """Get next available Run for Scan.

        Examples:
            ```python
                scan.get_next_run()
            ```

        Returns:
            A (Run) object manipulable
        """
        r = self.connexion.get('/sdk/v1/scan/{}/run/next'.format(self.id)).json()
        return Run(self.connexion, r["run"])

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete this scan from the platform.

        :warning: **DANGER ZONE**: Be very careful here!

        Examples:
            ```python
                scan.delete()
            ```
        """
        self.connexion.delete('/sdk/v1/scan/{}'.format(self.id))
        logger.info("Scan (id: {}) deleted from platform.".format(self.id))
