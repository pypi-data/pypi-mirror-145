import json

from fhire.exceptions import FhireError
from fhire.fhire_pojo.procedure.get_procedure import get_procedure_from_dict
from fhire.fhire_pojo.procedure.post_procedure import post_procedure_from_dict


class Procedure:

    def parse_https_get_procedure_response(self):
        try:
            return get_procedure_from_dict(json.loads(self.object))
        except AssertionError as e:
            raise FhireError(
                '{} Invalid response given to parse'.format(self.object)) from e

    def parse_https_post_procedure_response(self):
        try:
            return post_procedure_from_dict(json.loads(self.object))
        except AssertionError as e:
            raise FhireError(
                '{} Invalid response given to parse'.format(self.object)) from e
