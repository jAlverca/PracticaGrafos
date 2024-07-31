import math

from controls.dao.data_access_object import Data_Access_Object
from models.iglesia import Iglesia


class IglesiaDaoControl(Data_Access_Object):
    def __init__(self):
        super().__init__(Iglesia)
        self.__iglesia = None
        self.__grafoIgelsia = None

    @property
    def _iglesia(self):
        if self.__iglesia == None:
            self.__iglesia = Iglesia()
        return self.__iglesia

    @_iglesia.setter
    def _iglesia(self, value):
        self.__iglesia = value

    @property
    def save(self):
        self._iglesia._id = self._generate_id()
        self._save(self._iglesia)
        self.__iglesia = None

    def list(self):
        return self._list()

    def update(self, pos):
        self._merge(self._iglesia, pos)
        self.__iglesia = None

    def calcular_distancia(self, lat1, lon1, lat2, lon2):
        def grados_a_radianes(grados):
            return grados * (math.pi / 180)

        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])

        radio_tierra_km = 6378.137
        dlat = grados_a_radianes(lat2 - lat1)
        dlon = grados_a_radianes(lon2 - lon1)

        # Fórmula de Haversine
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(grados_a_radianes(lat1))
            * math.cos(grados_a_radianes(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia_km = radio_tierra_km * c

        return round(distancia_km, 3)
