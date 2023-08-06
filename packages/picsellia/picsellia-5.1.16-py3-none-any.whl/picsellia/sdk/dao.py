from picsellia.sdk.connexion import Connexion


class Dao:

    def __init__(self, connexion: Connexion, id: str) -> None:
        self._id = id
        self._connexion = connexion

    @property
    def connexion(self) -> Connexion:
        return self._connexion

    @property
    def id(self) -> Connexion:
        return self._id

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, type(self)):
            return self._id == __o.id and self._connexion == __o.connexion

        return False
