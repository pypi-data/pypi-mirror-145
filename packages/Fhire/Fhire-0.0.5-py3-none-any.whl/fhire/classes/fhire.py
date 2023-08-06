from typing import Any

from ..fhire_base.observation import Observation
from ..fhire_base.patient import Patient
from ..fhire_base.procedure import Procedure


class Fhire(Patient,Observation,Procedure):
    def __init__(self, object_under_test: Any):
        self.object = object_under_test



