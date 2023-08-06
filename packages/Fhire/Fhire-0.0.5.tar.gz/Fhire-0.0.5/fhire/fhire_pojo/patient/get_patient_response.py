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
#     result = _response_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Union, Optional, List, Any, TypeVar, Callable, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


class City(Enum):
    EINDHOVEN = "Eindhoven"
    GREENSBORO = "GREENSBORO"
    WESTFIELD = "Westfield"


class Line(Enum):
    HIGH_TECH_CAMPUS_37 = "High Tech Campus 37"
    THE_1099_ABERNATHY_BYPASS = "1099 Abernathy Bypass"
    THE_123_MAIN_STREET = "123 MAIN STREET"


class PostalCodeEnum(Enum):
    THE_01085 = "01085"
    THE_274011020 = "27401-1020"
    THE_5656_AE = "5656AE"


class State(Enum):
    MASSACHUSETTS = "Massachusetts"
    NB = "NB"
    NC = "NC"


class Use(Enum):
    HOME = "home"
    MOBILE = "mobile"
    OFFICIAL = "official"
    SECONDARY = "secondary"
    USUAL = "usual"
    WORK = "work"


@dataclass
class Address:
    postal_code: Union[PostalCodeEnum, int, None]
    use: Optional[Use] = None
    line: Optional[List[Line]] = None
    city: Optional[City] = None
    state: Optional[State] = None
    country: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Address':
        assert isinstance(obj, dict)
        postal_code = from_union([from_none, lambda x: from_union(
            [PostalCodeEnum, lambda x: int(x)], from_str(x))], obj.get("postalCode"))
        use = from_union([Use, from_none], obj.get("use"))
        line = from_union([lambda x: from_list(Line, x),
                          from_none], obj.get("line"))
        city = from_union([City, from_none], obj.get("city"))
        state = from_union([State, from_none], obj.get("state"))
        country = from_union([from_str, from_none], obj.get("country"))
        return Address(postal_code, use, line, city, state, country)

    def to_dict(self) -> dict:
        result: dict = {}
        result["postalCode"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: to_enum(
            PostalCodeEnum, (lambda x: is_type(PostalCodeEnum, x))(x)))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.postal_code)
        result["use"] = from_union(
            [lambda x: to_enum(Use, x), from_none], self.use)
        result["line"] = from_union([lambda x: from_list(
            lambda x: to_enum(Line, x), x), from_none], self.line)
        result["city"] = from_union(
            [lambda x: to_enum(City, x), from_none], self.city)
        result["state"] = from_union(
            [lambda x: to_enum(State, x), from_none], self.state)
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
class ContactName:
    text: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ContactName':
        assert isinstance(obj, dict)
        text = from_union([from_str, from_none], obj.get("text"))
        return ContactName(text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_union([from_str, from_none], self.text)
        return result


@dataclass
class Contact:
    name: Optional[ContactName] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Contact':
        assert isinstance(obj, dict)
        name = from_union([ContactName.from_dict, from_none], obj.get("name"))
        return Contact(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union(
            [lambda x: to_class(ContactName, x), from_none], self.name)
        return result


class Gender(Enum):
    FEMALE = "female"
    MALE = "male"


@dataclass
class Identifier:
    use: Optional[Use] = None
    type: Optional[MaritalStatus] = None
    system: Optional[str] = None
    value: Optional[str] = None
    rank: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Identifier':
        assert isinstance(obj, dict)
        use = from_union([Use, from_none], obj.get("use"))
        type = from_union(
            [MaritalStatus.from_dict, from_none], obj.get("type"))
        system = from_union([from_str, from_none], obj.get("system"))
        value = from_union([from_str, from_none], obj.get("value"))
        rank = from_union([from_int, from_none], obj.get("rank"))
        return Identifier(use, type, system, value, rank)

    def to_dict(self) -> dict:
        result: dict = {}
        result["use"] = from_union(
            [lambda x: to_enum(Use, x), from_none], self.use)
        result["type"] = from_union(
            [lambda x: to_class(MaritalStatus, x), from_none], self.type)
        result["system"] = from_union([from_str, from_none], self.system)
        result["value"] = from_union([from_str, from_none], self.value)
        result["rank"] = from_union([from_int, from_none], self.rank)
        return result


@dataclass
class ManagingOrganization:
    reference: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ManagingOrganization':
        assert isinstance(obj, dict)
        reference = from_union([from_str, from_none], obj.get("reference"))
        return ManagingOrganization(reference)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reference"] = from_union([from_str, from_none], self.reference)
        return result


@dataclass
class ResourceMeta:
    version_id: Optional[UUID] = None
    last_updated: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResourceMeta':
        assert isinstance(obj, dict)
        version_id = from_union(
            [lambda x: UUID(x), from_none], obj.get("versionId"))
        last_updated = from_union(
            [from_datetime, from_none], obj.get("lastUpdated"))
        return ResourceMeta(version_id, last_updated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["versionId"] = from_union(
            [lambda x: str(x), from_none], self.version_id)
        result["lastUpdated"] = from_union(
            [lambda x: x.isoformat(), from_none], self.last_updated)
        return result


@dataclass
class NameElement:
    use: Optional[Use] = None
    family: Optional[str] = None
    given: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'NameElement':
        assert isinstance(obj, dict)
        use = from_union([Use, from_none], obj.get("use"))
        family = from_union([from_str, from_none], obj.get("family"))
        given = from_union([lambda x: from_list(
            from_str, x), from_none], obj.get("given"))
        return NameElement(use, family, given)

    def to_dict(self) -> dict:
        result: dict = {}
        result["use"] = from_union(
            [lambda x: to_enum(Use, x), from_none], self.use)
        result["family"] = from_union([from_str, from_none], self.family)
        result["given"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.given)
        return result


class ResourceType(Enum):
    PATIENT = "Patient"


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
class Resource:
    resource_type: Optional[ResourceType] = None
    id: Optional[UUID] = None
    meta: Optional[ResourceMeta] = None
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[NameElement]] = None
    telecom: Optional[List[Identifier]] = None
    gender: Optional[Gender] = None
    birth_date: Optional[datetime] = None
    address: Optional[List[Address]] = None
    multiple_birth_integer: Optional[int] = None
    contact: Optional[List[Contact]] = None
    communication: Optional[List[Communication]] = None
    managing_organization: Optional[ManagingOrganization] = None
    active: Optional[bool] = None
    text: Optional[Text] = None
    marital_status: Optional[MaritalStatus] = None
    multiple_birth_boolean: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Resource':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [ResourceType, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union([ResourceMeta.from_dict, from_none], obj.get("meta"))
        identifier = from_union([lambda x: from_list(
            Identifier.from_dict, x), from_none], obj.get("identifier"))
        name = from_union([lambda x: from_list(
            NameElement.from_dict, x), from_none], obj.get("name"))
        telecom = from_union([lambda x: from_list(
            Identifier.from_dict, x), from_none], obj.get("telecom"))
        gender = from_union([Gender, from_none], obj.get("gender"))
        birth_date = from_union(
            [from_datetime, from_none], obj.get("birthDate"))
        address = from_union([lambda x: from_list(
            Address.from_dict, x), from_none], obj.get("address"))
        multiple_birth_integer = from_union(
            [from_int, from_none], obj.get("multipleBirthInteger"))
        contact = from_union([lambda x: from_list(
            Contact.from_dict, x), from_none], obj.get("contact"))
        communication = from_union([lambda x: from_list(
            Communication.from_dict, x), from_none], obj.get("communication"))
        managing_organization = from_union(
            [ManagingOrganization.from_dict, from_none], obj.get("managingOrganization"))
        active = from_union([from_bool, from_none], obj.get("active"))
        text = from_union([Text.from_dict, from_none], obj.get("text"))
        marital_status = from_union(
            [MaritalStatus.from_dict, from_none], obj.get("maritalStatus"))
        multiple_birth_boolean = from_union(
            [from_bool, from_none], obj.get("multipleBirthBoolean"))
        return Resource(resource_type, id, meta, identifier, name, telecom, gender, birth_date, address, multiple_birth_integer, contact, communication, managing_organization, active, text, marital_status, multiple_birth_boolean)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [lambda x: to_enum(ResourceType, x), from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(ResourceMeta, x), from_none], self.meta)
        result["identifier"] = from_union([lambda x: from_list(
            lambda x: to_class(Identifier, x), x), from_none], self.identifier)
        result["name"] = from_union([lambda x: from_list(
            lambda x: to_class(NameElement, x), x), from_none], self.name)
        result["telecom"] = from_union([lambda x: from_list(
            lambda x: to_class(Identifier, x), x), from_none], self.telecom)
        result["gender"] = from_union(
            [lambda x: to_enum(Gender, x), from_none], self.gender)
        result["birthDate"] = from_union(
            [lambda x: x.isoformat(), from_none], self.birth_date)
        result["address"] = from_union([lambda x: from_list(
            lambda x: to_class(Address, x), x), from_none], self.address)
        result["multipleBirthInteger"] = from_union(
            [from_int, from_none], self.multiple_birth_integer)
        result["contact"] = from_union([lambda x: from_list(
            lambda x: to_class(Contact, x), x), from_none], self.contact)
        result["communication"] = from_union([lambda x: from_list(
            lambda x: to_class(Communication, x), x), from_none], self.communication)
        result["managingOrganization"] = from_union([lambda x: to_class(
            ManagingOrganization, x), from_none], self.managing_organization)
        result["active"] = from_union([from_bool, from_none], self.active)
        result["text"] = from_union(
            [lambda x: to_class(Text, x), from_none], self.text)
        result["maritalStatus"] = from_union(
            [lambda x: to_class(MaritalStatus, x), from_none], self.marital_status)
        result["multipleBirthBoolean"] = from_union(
            [from_bool, from_none], self.multiple_birth_boolean)
        return result


class Mode(Enum):
    MATCH = "match"


@dataclass
class Search:
    mode: Optional[Mode] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Search':
        assert isinstance(obj, dict)
        mode = from_union([Mode, from_none], obj.get("mode"))
        return Search(mode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mode"] = from_union(
            [lambda x: to_enum(Mode, x), from_none], self.mode)
        return result


@dataclass
class Entry:
    full_url: Optional[str] = None
    resource: Optional[Resource] = None
    search: Optional[Search] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Entry':
        assert isinstance(obj, dict)
        full_url = from_union([from_str, from_none], obj.get("fullUrl"))
        resource = from_union(
            [Resource.from_dict, from_none], obj.get("resource"))
        search = from_union([Search.from_dict, from_none], obj.get("search"))
        return Entry(full_url, resource, search)

    def to_dict(self) -> dict:
        result: dict = {}
        result["fullUrl"] = from_union([from_str, from_none], self.full_url)
        result["resource"] = from_union(
            [lambda x: to_class(Resource, x), from_none], self.resource)
        result["search"] = from_union(
            [lambda x: to_class(Search, x), from_none], self.search)
        return result


@dataclass
class Link:
    relation: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Link':
        assert isinstance(obj, dict)
        relation = from_union([from_str, from_none], obj.get("relation"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Link(relation, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["relation"] = from_union([from_str, from_none], self.relation)
        result["url"] = from_union([from_str, from_none], self.url)
        return result


@dataclass
class GetPatientMeta:
    last_updated: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GetPatientMeta':
        assert isinstance(obj, dict)
        last_updated = from_union(
            [from_datetime, from_none], obj.get("lastUpdated"))
        return GetPatientMeta(last_updated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lastUpdated"] = from_union(
            [lambda x: x.isoformat(), from_none], self.last_updated)
        return result


@dataclass
class GetPatient:
    resource_type: Optional[str] = None
    id: Optional[UUID] = None
    meta: Optional[GetPatientMeta] = None
    type: Optional[str] = None
    link: Optional[List[Link]] = None
    entry: Optional[List[Entry]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GetPatient':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [from_str, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union(
            [GetPatientMeta.from_dict, from_none], obj.get("meta"))
        type = from_union([from_str, from_none], obj.get("type"))
        link = from_union([lambda x: from_list(
            Link.from_dict, x), from_none], obj.get("link"))
        entry = from_union([lambda x: from_list(
            Entry.from_dict, x), from_none], obj.get("entry"))
        return GetPatient(resource_type, id, meta, type, link, entry)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [from_str, from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(GetPatientMeta, x), from_none], self.meta)
        result["type"] = from_union([from_str, from_none], self.type)
        result["link"] = from_union([lambda x: from_list(
            lambda x: to_class(Link, x), x), from_none], self.link)
        result["entry"] = from_union([lambda x: from_list(
            lambda x: to_class(Entry, x), x), from_none], self.entry)
        return result


def get_patient_response_from_dict(s: Any) -> GetPatient:
    return GetPatient.from_dict(s)


def get_patient_response_to_dict(x: GetPatient) -> Any:
    return to_class(GetPatient, x)


