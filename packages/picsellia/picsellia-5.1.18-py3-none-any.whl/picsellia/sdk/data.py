from functools import partial
import json
import logging
import os
import sys
from time import sleep
from typing import List, Union
from beartype import beartype
from picsellia.types.schemas import DataSchema
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia.decorators import exception_handler
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
from picsellia.sdk.multi_object import MultiObject
from picsellia import exceptions as exceptions
from picsellia import pxl_multithreading as mlt

logger = logging.getLogger('picsellia')


class Data(Dao):

    def __init__(self, connexion: Connexion, datalake_id: str, data: dict):
        object = DataSchema(**data)
        super().__init__(connexion, object.picture_id)
        self._datalake_id = datalake_id
        self._external_url = object.external_url
        self._internal_key = object.internal_key

    def __str__(self,): return "{}Data{} object (id: {})".format(bcolors.GREEN, bcolors.ENDC, self.id)

    @property
    def datalake_id(self) -> str:
        return self._datalake_id

    @property
    def external_url(self) -> str:
        return self._external_url

    @property
    def internal_key(self) -> str:
        return self._internal_key

    @exception_handler
    @beartype
    def add_tags(self, tags: Union[str, List[str]]) -> None:
        """Add some tags to data

        You can give a string, a list of string.

        Examples:
            ```python
                data.add_tags("bicyle")
                data.add_tags(["car", "truck", "plane"])
            ```
        """
        if isinstance(tags, str):
            tags = [tags]

        assert tags != [], "Given tags are empty. They can't be empty"
        data = {
            'tags': tags,
            'data_ids': [self.id]
        }
        self.connexion.post('/sdk/v1/datalake/{}/data/tags'.format(self.datalake_id), data=json.dumps(data))
        logger.info("{} tags added to data (id: {}) in datalake {}.".format(len(tags), self.id, self.datalake_id))

    @exception_handler
    @beartype
    def remove_tags(self, tags: Union[str, List[str]]) -> None:
        """Remove some tags of a data

        You can give a string or a list of string.

        Examples:
            ```python
                data.remove_tags("plane")
                data.remove_tags(["truck", "car"])
            ```
        """
        if isinstance(tags, str):
            tags = [tags]

        assert tags != [], "Given tags are empty. They can't be empty"
        data = {
            'tags': tags,
            'data_ids': [self.id]
        }
        self.connexion.delete('/sdk/v1/datalake/{}/data/tags'.format(self.datalake_id), data=json.dumps(data))
        logger.info("{} tags removed from data (id: {}) in datalake {}.".format(len(tags), self.id, self.datalake_id))

    @exception_handler
    @beartype
    def get_tags(self,) -> List[str]:
        """Retrieve the tags of your data.

        Examples:
            ```python
                tags = data.get_tags()
                assert tags == ["bicyle"]
            ```

        Returns:
            List of tags as strings
        """
        r = self.connexion.get('/sdk/v1/datalake/{}/data/{}/tags'.format(self.datalake_id, self.id)).json()
        return r["tags"]

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete data and remove it from datalake.

        :warning: **DANGER ZONE**: Be very careful here!

        Remove this data from datalake, and all of the picture linked to this data.

        Examples:
            ```python
                data.delete()
            ```
        """
        data = {
            'data_ids': [self.id]
        }
        self.connexion.delete('/sdk/v1/datalake/{}/data/delete'.format(self.datalake_id), data=json.dumps(data))
        logger.info("1 asset (id: {}) deleted from datalake {}.".format(self.id, self.datalake_id))


    @exception_handler
    @beartype
    def download(self, target_path : str = './') -> None:
        """Download

        Examples:
            ```python
                data = clt.get_datalake().fetch_data(1)
                data.download('./pictures/')
            ```

        Arguments:
            target_path (str, optional): Target path where data will be downloaded. Defaults to './'.
        """
        path = os.path.join(target_path, self.external_url)
        if self.connexion.download_some_file(False, self.internal_key, path, False):
            logger.info('{} downloaded successfully'.format(self.external_url))
        else:
            logger.error("Could not download {} file".format(self.internal_key))

class MultiData(MultiObject[Data]):

    @beartype
    def __init__(self, connexion: Connexion, datalake_id: str, items: List[Data]):
        super().__init__(connexion, items)
        self.datalake_id = datalake_id

    def __str__(self,): return "{}MultiData{} object, size: {}".format(bcolors.GREEN, bcolors.ENDC,len(self))

    def __getitem__(self, key) -> Union[Data, 'MultiData']:
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            data = [self.items[i] for i in indices]
            return MultiData(self.connexion, self.datalake_id, data)
        return self.items[key]

    @beartype
    def __add__(self, other):
        self.assert_same_connexion(other)
        items = self.items.copy()
        if isinstance(other, MultiData):
            items.extend(other.items.copy())
        elif isinstance(other, Data):
            items.append(other)
        else:
            raise exceptions.PicselliaError("You can't add these two objects")

        return MultiData(self.connexion, self.datalake_id, items)

    @beartype
    def __iadd__(self, other):
        self.assert_same_connexion(other)

        if isinstance(other, MultiData):
            self.extend(other.items.copy())
        elif isinstance(other, Data):
            self.append(other)
        else:
            raise exceptions.PicselliaError("You can't add these two objects")

        return self


    def copy(self):
        return MultiData(self.connexion, self.datalake_id, self.items.copy())

    @exception_handler
    @beartype
    def add_tags(self, tags: Union[str, List[str]]) -> None:
        """Add some tags to a bunch of data

        You can give a string, a list of string.

        Examples:
            ```python
                whole_data = datalake.fecth_data()
                whole_data.add_tags("never")
                whole_data.add_tags(["gonna", "give", "you", "up"])
            ```
        """
        if isinstance(tags, str):
            tags = [tags]
        assert tags != [], "Given tags are empty. They can't be empty"
        payload = {
            'tags': tags,
            'data_ids': [data.id for data in self.items]
        }
        self.connexion.post('/sdk/v1/datalake/{}/data/tags'.format(self.datalake_id), data=json.dumps(payload))
        logger.info("{} tags added to {} data in datalake {}."
                    .format(len(tags), len(self.items), self.datalake_id))

    @exception_handler
    @beartype
    def remove_tags(self, tags: Union[str, List[str]]) -> None:
        """Remove some tags on a list of data

        You can give a string, a list of string.

        Examples:
            ```python
                whole_data = datalake.fecth_data()
                whole_data.remove_tags("gonna")
                whole_data.remove_tags(["you"])
            ```
        """
        if isinstance(tags, str):
            tags = [tags]

        assert tags != [], "Given tags are empty. They can't be empty"
        data = {
            'tags': tags,
            'data_ids': [data.id for data in self.items]
        }
        self.connexion.delete('/sdk/v1/datalake/{}/data/tags'.format(self.datalake_id), data=json.dumps(data))
        logger.info("{} tags removed from {} data in datalake {}."
                    .format(len(tags), len(self.items), self.datalake_id))

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete a bunch of data and remove them from datalake.

        :warning: **DANGER ZONE**: Be very careful here!

        Remove a bunch of data from datalake, and all of the picture linked to all data.

        Examples:
            ```python
                whole_data = datalake.fetch_data(quantity=3)
                whole_data.delete()
            ```
        """
        data = {
            'data_ids': [data.id for data in self.items]
        }
        self.connexion.delete('/sdk/v1/datalake/{}/data/delete'.format(self.datalake_id), data=json.dumps(data))
        logger.info("{} data deleted from datalake {}.".format(len(self.items), self.datalake_id))

    @exception_handler
    @beartype
    def download(self, target_path: str = './', nb_threads: int = 20) -> None:
        """Download this multi data in given target path


        Examples:
            ```python
                bunch_of_data = client.get_datalake().fetch_data(25)
                bunch_of_data.download('./downloads/')
            ```
        Arguments:
            target_path (str, optional): Target path where to download. Defaults to './'.
            nb_threads (int, optional): Number of threads used to download. Defaults to 20.
        """
        f = partial(mlt.mlt_download_list_data_or_pics, self.connexion, self.datalake_id, target_path)
        mlt.do_multiprocess_things(f, self.items, nb_threads)
        logger.info("{} downloaded in {}".format(len(self.items), target_path))
