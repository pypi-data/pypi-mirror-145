from beartype import beartype
from picsellia.decorators import exception_handler
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia.types.schemas import OrganizationSchema


class Organization(Dao):

    def __init__(self, connexion: Connexion, data: dict):
        organization = OrganizationSchema(**data)
        super().__init__(connexion, organization.id)
        self._name = organization.name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self,): return "{}Organization '{}' {} (id: {})".format(bcolors.BOLD, self.name, bcolors.ENDC, self.id)

    @exception_handler
    @beartype
    def get_resource_url_on_platform(self,) -> str:
        """Get platform url of this resource.

        Examples:
            ```python
                print(foo_dataset.get_resource_url_on_platform())
                >>> https://app.picsellia.com/organization/62cffb84-b92c-450c-bc37-8c4dd4d0f590
            ```

        Returns:
            Url on Platform for this resource
        """

        return "{}/organization/{}".format(self.connexion.host, self.id)

    @exception_handler
    @beartype
    def get_infos(self) -> dict:
        """Return some information about this organization

        Examples:
            ```python
                org = client.get_organization()
                print(org.get_infos())
            ```

        Returns:
            A dict with id and name of the organization
        """
        return {"id": self.id, "name": self.name}
