
from beartype import beartype
from picsellia.decorators import exception_handler
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia.types.schemas import WorkerSchema

class Worker(Dao):

    def __init__(self, connexion: Connexion, data: dict):
        worker = WorkerSchema(**data)
        super().__init__(connexion, worker.id)
        self._username = worker.user.username

    @property
    def username(self) -> str:
        return self._username

    def __str__(self,): return "{}Worker '{}' {}".format(bcolors.UNDERLINE, self.username, bcolors.ENDC)

    @exception_handler
    @beartype
    def get_infos(self) -> dict:
        """Retrieve worker info

        Examples:
            ```python
                worker = project.list_workers()[0]
                print(worker.get_infos())
            ```

        Returns:
            A dict with data of the worker
        """
        return {"username": self.username}
