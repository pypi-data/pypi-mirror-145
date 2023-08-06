# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = create_patient_response_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


@dataclass
class Address:
    line: Optional[List[str]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        line = from_union([lambda x: from_list(from_str, x),
                          from_none], obj.get("line"))
        city = from_union([from_str, from_none], obj.get("city"))
        state = from_union([from_str, from_none], obj.get("state"))
        postal_code = from_union([from_str, from_none], obj.get("postalCode"))
        country = from_union([from_str, from_none], obj.get("country"))
        return Address(line, city, state, postal_code, country)

    def to_dict(self) -> dict:
        result: dict = {}
        result["line"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.line)
        result["city"] = from_union([from_str, from_none], self.city)
        result["state"] = from_union([from_str, from_none], self.state)
        result["postalCode"] = from_union(
            [from_str, from_none], self.postal_code)
        result["country"] = from_union([from_str, from_none], self.country)
        return result


@dataclass
class Coding:
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Coding':
        assert isinstance(obj, dict)
        system = from_union([from_str, from_none], obj.get("system"))
        code = from_union([from_str, from_none], obj.get("code"))
        display = from_union([from_str, from_none], obj.get("display"))
        return Coding(system, code, display)

    def to_dict(self) -> dict:
        result: dict = {}
        result["system"] = from_union([from_str, from_none], self.system)
        result["code"] = from_union([from_str, from_none], self.code)
        result["display"] = from_union([from_str, from_none], self.display)
        return result


@dataclass
class MaritalStatus:
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MaritalStatus':
        assert isinstance(obj, dict)
        coding = from_union([lambda x: from_list(
            Coding.from_dict, x), from_none], obj.get("coding"))
        text = from_union([from_str, from_none], obj.get("text"))
        return MaritalStatus(coding, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coding"] = from_union([lambda x: from_list(
            lambda x: to_class(Coding, x), x), from_none], self.coding)
        result["text"] = from_union([from_str, from_none], self.text)
        return result


@dataclass
class Communication:
    language: Optional[MaritalStatus] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Communication':
        assert isinstance(obj, dict)
        language = from_union(
            [MaritalStatus.from_dict, from_none], obj.get("language"))
        return Communication(language)

    def to_dict(self) -> dict:
        result: dict = {}
        result["language"] = from_union(
            [lambda x: to_class(MaritalStatus, x), from_none], self.language)
        return result


@dataclass
class Identifier:
    system: Optional[str] = None
    value: Optional[str] = None
    type: Optional[MaritalStatus] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Identifier':
        assert isinstance(obj, dict)
        system = from_union([from_str, from_none], obj.get("system"))
        value = from_union([from_str, from_none], obj.get("value"))
        type = from_union(
            [MaritalStatus.from_dict, from_none], obj.get("type"))
        return Identifier(system, value, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["system"] = from_union([from_str, from_none], self.system)
        result["value"] = from_union([from_str, from_none], self.value)
        result["type"] = from_union(
            [lambda x: to_class(MaritalStatus, x), from_none], self.type)
        return result


@dataclass
class Meta:
    version_id: Optional[UUID] = None
    last_updated: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Meta':
        assert isinstance(obj, dict)
        version_id = from_union(
            [lambda x: UUID(x), from_none], obj.get("versionId"))
        last_updated = from_union(
            [from_datetime, from_none], obj.get("lastUpdated"))
        return Meta(version_id, last_updated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["versionId"] = from_union(
            [lambda x: str(x), from_none], self.version_id)
        result["lastUpdated"] = from_union(
            [lambda x: x.isoformat(), from_none], self.last_updated)
        return result


@dataclass
class Name:
    use: Optional[str] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Name':
        assert isinstance(obj, dict)
        use = from_union([from_str, from_none], obj.get("use"))
        family = from_union([from_str, from_none], obj.get("family"))
        given = from_union([lambda x: from_list(
            from_str, x), from_none], obj.get("given"))
        return Name(use, family, given)

    def to_dict(self) -> dict:
        result: dict = {}
        result["use"] = from_union([from_str, from_none], self.use)
        result["family"] = from_union([from_str, from_none], self.family)
        result["given"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.given)
        return result


@dataclass
class Telecom:
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Telecom':
        assert isinstance(obj, dict)
        system = from_union([from_str, from_none], obj.get("system"))
        value = from_union([from_str, from_none], obj.get("value"))
        use = from_union([from_str, from_none], obj.get("use"))
        return Telecom(system, value, use)

    def to_dict(self) -> dict:
        result: dict = {}
        result["system"] = from_union([from_str, from_none], self.system)
        result["value"] = from_union([from_str, from_none], self.value)
        result["use"] = from_union([from_str, from_none], self.use)
        return result


@dataclass
class Text:
    status: Optional[str] = None
    div: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Text':
        assert isinstance(obj, dict)
        status = from_union([from_str, from_none], obj.get("status"))
        div = from_union([from_str, from_none], obj.get("div"))
        return Text(status, div)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = from_union([from_str, from_none], self.status)
        result["div"] = from_union([from_str, from_none], self.div)
        return result


@dataclass
class CdrCreatePatientResponse:
    resource_type: Optional[str] = None
    id: Optional[UUID] = None
    meta: Optional[Meta] = None
    text: Optional[Text] = None
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[Name]] = None
    telecom: Optional[List[Telecom]] = None
    gender: Optional[str] = None
    birth_date: Optional[datetime] = None
    address: Optional[List[Address]] = None
    marital_status: Optional[MaritalStatus] = None
    multiple_birth_boolean: Optional[bool] = None
    communication: Optional[List[Communication]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CdrCreatePatientResponse':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [from_str, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union([Meta.from_dict, from_none], obj.get("meta"))
        text = from_union([Text.from_dict, from_none], obj.get("text"))
        identifier = from_union([lambda x: from_list(
            Identifier.from_dict, x), from_none], obj.get("identifier"))
        name = from_union([lambda x: from_list(
            Name.from_dict, x), from_none], obj.get("name"))
        telecom = from_union([lambda x: from_list(
            Telecom.from_dict, x), from_none], obj.get("telecom"))
        gender = from_union([from_str, from_none], obj.get("gender"))
        birth_date = from_union(
            [from_datetime, from_none], obj.get("birthDate"))
        address = from_union([lambda x: from_list(
            Address.from_dict, x), from_none], obj.get("address"))
        marital_status = from_union(
            [MaritalStatus.from_dict, from_none], obj.get("maritalStatus"))
        multiple_birth_boolean = from_union(
            [from_bool, from_none], obj.get("multipleBirthBoolean"))
        communication = from_union([lambda x: from_list(
            Communication.from_dict, x), from_none], obj.get("communication"))
        return CdrCreatePatientResponse(resource_type, id, meta, text, identifier, name, telecom, gender, birth_date, address, marital_status, multiple_birth_boolean, communication)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [from_str, from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(Meta, x), from_none], self.meta)
        result["text"] = from_union(
            [lambda x: to_class(Text, x), from_none], self.text)
        result["identifier"] = from_union([lambda x: from_list(
            lambda x: to_class(Identifier, x), x), from_none], self.identifier)
        result["name"] = from_union([lambda x: from_list(
            lambda x: to_class(Name, x), x), from_none], self.name)
        result["telecom"] = from_union([lambda x: from_list(
            lambda x: to_class(Telecom, x), x), from_none], self.telecom)
        result["gender"] = from_union([from_str, from_none], self.gender)
        result["birthDate"] = from_union(
            [lambda x: x.isoformat(), from_none], self.birth_date)
        result["address"] = from_union([lambda x: from_list(
            lambda x: to_class(Address, x), x), from_none], self.address)
        result["maritalStatus"] = from_union(
            [lambda x: to_class(MaritalStatus, x), from_none], self.marital_status)
        result["multipleBirthBoolean"] = from_union(
            [from_bool, from_none], self.multiple_birth_boolean)
        result["communication"] = from_union([lambda x: from_list(
            lambda x: to_class(Communication, x), x), from_none], self.communication)
        return result


def create_patient_response_from_dict(s: Any) -> CdrCreatePatientResponse:
    return CdrCreatePatientResponse.from_dict(s)


def create_patient_response_to_dict(x: CdrCreatePatientResponse) -> Any:
    return to_class(CdrCreatePatientResponse, x)
