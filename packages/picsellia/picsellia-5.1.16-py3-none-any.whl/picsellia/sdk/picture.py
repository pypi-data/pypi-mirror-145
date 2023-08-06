from datetime import date
from functools import partial
import json
import logging
import os
from typing import Dict, List, Union
from beartype import beartype
from picsellia.decorators import exception_handler
from picsellia.sdk.connexion import Connexion
from picsellia.sdk.dao import Dao
from picsellia.sdk.multi_object import MultiObject
import picsellia.exceptions as exceptions
from picsellia.types.schemas import PictureSchema
from picsellia.bcolors import bcolors
import warnings
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
warnings.filterwarnings("ignore", category=BeartypeDecorHintPep585DeprecationWarning)
from picsellia import pxl_multithreading as mlt

logger = logging.getLogger('picsellia')


class Picture(Dao):

    def __init__(self, connexion: Connexion, data: dict):
        picture = PictureSchema(**data)
        super().__init__(connexion, picture.picture_id)
        self._external_url = picture.external_url
        self._internal_key = picture.internal_key
        self._width = picture.width
        self._height = picture.height
        self._tags = picture.tags

    @property
    def external_url(self) -> str:
        return self._external_url

    @property
    def internal_key(self) -> str:
        return self._internal_key

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def tags(self) -> List[str]:
        assert self._tags != None, "Tags were not retrieved, please retrieve this picture again"
        return self._tags

    def __str__(self,): return "{}Picture '{}' {} (id: {})".format(bcolors.YELLOW, self.external_url, bcolors.ENDC, self.id)

    @exception_handler
    @beartype
    def add_annotation(self, data: List[dict], creation_date: date = None, duration: float = None,
                       reviewed: bool = None, is_accepted: bool = None, is_skipped: bool = None,
                       nb_instances: int = None) -> None:
        """Add annotation to this picture.

        Data of annotation is mandatory and its type will be checked here before sending it to platform.
        Other information will be stored in Picsellia database.

        Examples:
            ```
                data = [{
                    "type":"rectangle",
                    "label":"car",
                    "rectangle":{
                        "top":45,
                        "left":120,
                        "width":50,
                        "height":50
                    }
                }]
                pic.add_annotation(data)
            ```
        Arguments:
            data (List[dict]): List of annotations.
            creation_date (date, optional): Creation date; Shall be a 'date' type. Defaults to None.
            duration (float, optional): Duration. Defaults to None.
            reviewed (bool, optional): Reviewed. Defaults to None.
            is_accepted (bool, optional): Is accepted. Defaults to None.
            is_skipped (bool, optional): Is skipped. Defaults to None.
            nb_instances (int, optional): Number of instances. Defaults to None.

        Raises:
            exceptions.TyperError: When annotation is not parsable
        """
        if data == []:
            raise exceptions.TyperError("Data shall not be empty")

        for annot in data:
            if annot == {}:
                raise exceptions.TyperError("An annotation shall not be empty")
            annot_keys = annot.keys()
            if "type" not in annot_keys:
                raise exceptions.TyperError(
                    "'type' key missing from object {}".format(annot))
            supported_types = ["classification", "rectangle", "polygon"]
            if annot["type"] not in supported_types:
                raise exceptions.TyperError(
                    "type must be of {}, found '{}'".format(supported_types, annot["type"]))
            if "label" not in annot_keys:
                raise exceptions.TyperError(
                    "'label' key missing from object {}".format(annot))
            if annot["type"] == "classification":
                pass
            elif annot["type"] == "rectangle":
                if "rectangle" not in annot_keys:
                    raise exceptions.TyperError(
                        "missing 'rectangle' key for object {}".format(annot))
                rect = annot["rectangle"]
                if "top" not in rect.keys():
                    raise exceptions.TyperError(
                        "missing 'top' key in rectangle for object {}".format(annot))
                if "left" not in rect.keys():
                    raise exceptions.TyperError(
                        "missing 'left' key in rectangle for object {}".format(annot))
                if "width" not in rect.keys():
                    raise exceptions.TyperError(
                        "missing 'width' key in rectangle for object {}".format(annot))
                if "height" not in rect.keys():
                    raise exceptions.TyperError(
                        "missing 'height' key in rectangle for object {}".format(annot))
            elif annot["type"] == "polygon":
                if "polygon" not in annot_keys:
                    raise exceptions.TyperError(
                        "missing 'polygon' key for object {}".format(annot))
                poly = annot["polygon"]
                if type(poly) != dict:
                    raise exceptions.TyperError(
                        "'polygon' must be a dict, not {}".format(type(poly)))
                if "geometry" not in poly.keys():
                    raise exceptions.TyperError(
                        "missing 'geometry' key in 'polygon' for object {}".format(annot))
                geometry = poly["geometry"]
                if type(geometry) != list:
                    raise exceptions.TyperError(
                        "'geometry' must be a list, not {}".format(type(geometry)))
                if len(geometry) < 3:
                    raise exceptions.TyperError(
                        "polygons can't have less than 3 points")
                for coords in geometry:
                    if type(coords) != dict:
                        raise exceptions.TyperError(
                            "coordinates in 'geometry' must be a dict, not {}".format(type(coords)))
                    if 'x' not in coords.keys():
                        raise exceptions.TyperError(
                            "missing 'x' coordinate in 'geometry' for object {}".format(annot))
                    if 'y' not in coords.keys():
                        raise exceptions.TyperError(
                            "missing 'y' coordinate in 'geometry' for object {}".format(annot))

        payload = {"data": data}
        if creation_date is not None:
            payload["creation_date"] = creation_date.isoformat()
        if duration is not None:
            payload["duration"] = duration
        if reviewed is not None:
            payload["reviewed"] = reviewed
        if is_accepted is not None:
            payload["is_accepted"] = is_accepted
        if is_skipped is not None:
            payload["is_skipped"] = is_skipped
        if nb_instances is not None:
            payload["nb_instances"] = nb_instances
        self.connexion.put('/sdk/v1/picture/{}/annotations'.format(self.id), data=json.dumps(payload)).json()

    @exception_handler
    @beartype
    def delete_annotations(self,) -> None:
        """Delete all annotations of a picture.

        :warning: **DANGER ZONE**: Be careful here !

        Examples:
            ```python
                pic.delete_annotations()
            ```
        """
        self.connexion.delete('/sdk/v1/picture/{}/annotations'.format(self.id))

    @exception_handler
    @beartype
    def list_annotations(self,) -> List[Dict]:
        """List all annotation of a picture

        Examples:
            ```python
                annotations = pic.list_annotations()
            ```

        Returns:
            A list of dict representing annotations
        """
        r = self.connexion.get('/sdk/v1/picture/{}/annotations'.format(self.id)).json()
        return r["annotations"]

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete picture from its dataset

        :warning: **DANGER ZONE**: Be very careful here!

        Remove this picture and its annotation from the dataset it belongs

        Examples:
            ```python
                pic.delete()
            ```
        """
        self.connexion.delete('/sdk/v1/picture/{}'.format(self.id))
        logger.info("Picture {} removed from dataset".format(self.id))

    @exception_handler
    @beartype
    def download(self, target_path : str = './') -> None:
        """Download this picture into given target path

        Examples:
            ```python
                pic = foo_dataset.get_picture('bar.png')
                pic.download('./pictures/')
            ```

        Arguments:
            target_path (str, optional): Target path where picture will be downloaded. Defaults to './'.
        """
        path = os.path.join(target_path, self.external_url)
        if self.connexion.download_some_file(False, self.internal_key, path, False):
            logger.info('{} downloaded successfully'.format(self.external_url))
        else:
            logger.error("Could not download {} file".format(self.internal_key))


class MultiPicture(MultiObject[Picture]):

    @beartype
    def __init__(self, connexion: Connexion, dataset_id: str, items: List[Picture]):
        super().__init__(connexion, items)
        self.dataset_id = dataset_id
    
    def __str__(self,): return "{}MultiPicture{} object, size: {}".format(bcolors.GREEN, bcolors.ENDC,len(self))

    def __getitem__(self, key) -> Union[Picture, 'MultiPicture']:
        if isinstance(key, slice):
            indices = range(*key.indices(len(self.items)))
            pictures = [self.items[i] for i in indices]
            return MultiPicture(self.connexion, self.dataset_id, pictures)
        return self.items[key]
    
    @beartype
    def __add__(self, other):
        self.assert_same_connexion(other)
        items = self.items.copy()
        if isinstance(other, MultiPicture):
            items.extend(other.items.copy())
        elif isinstance(other, Picture):
            items.append(other)
        else:
            raise exceptions.PicselliaError("You can't add these two objects")

        return MultiPicture(self.connexion, self.dataset_id, items)

    @beartype
    def __iadd__(self, other):
        self.assert_same_connexion(other)

        if isinstance(other, MultiPicture):
            self.extend(other.items.copy())
        elif isinstance(other, Picture):
            self.append(other)
        else:
            raise exceptions.PicselliaError("You can't add these two objects")

        return self

    def copy(self):
        return MultiPicture(self.connexion, self.dataset_id, self.items.copy())

    @exception_handler
    @beartype
    def delete(self,) -> None:
        """Delete pictures from their dataset

        :warning: **DANGER ZONE**: Be very careful here!

        Remove this picture and its annotation from the dataset it belongs

        Examples:
            ```python
                pics = dataset.list_pictures()
                pics.delete()
            ```
        """
        payload = {'to_delete': [pic.id for pic in self.items]}
        self.connexion.delete('/sdk/v1/dataset/{}/pictures'.format(self.dataset_id), data=json.dumps(payload))
        logger.info("{} pictures removed from dataset {}".format(len(self.items), self.dataset_id))

    @exception_handler
    @beartype
    def download(self, target_path: str = './', nb_threads: int = 20) -> None:
        """Download this multi picture in given target path


        Examples:
            ```python
                bunch_of_pics = client.get_dataset("foo_dataset").list_pictures()
                bunch_of_pics.download('./downloads/')
            ```
        Arguments:
            target_path (str, optional): Target path where to download. Defaults to './'.
            nb_threads (int, optional): Number of threads used to download. Defaults to 20.
        """
        f = partial(mlt.mlt_download_list_data_or_pics, self.connexion, self.dataset_id, target_path)
        mlt.do_multiprocess_things(f, self.items, nb_threads)
        logger.info("{} downloaded in {}".format(len(self.items), target_path))
