import json

from fhire.exceptions import FhireError
from fhire.fhire_pojo.observation.get_observation import get_observation_from_dict
from fhire.fhire_pojo.observation.post_observation import post_observation_from_dict


class Observation:

    def parse_https_get_procedure_response(self):
        try:
            return get_observation_from_dict(json.loads(self.object))
        except AssertionError as e:
            raise FhireError(
                '{} Invalid response given to parse'.format(self.object)) from e

    def parse_https_post_procedure_response(self):
        try:
            return post_observation_from_dict(json.loads(self.object))
        except AssertionError as e:
            raise FhireError(
                '{} Invalid response given to parse'.format(self.object)) from e
