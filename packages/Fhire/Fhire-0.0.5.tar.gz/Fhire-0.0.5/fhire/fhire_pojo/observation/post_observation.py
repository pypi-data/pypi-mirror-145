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
#     result = post_observation_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


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
class Code:
    coding: Optional[List[Coding]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Code':
        assert isinstance(obj, dict)
        coding = from_union([lambda x: from_list(
            Coding.from_dict, x), from_none], obj.get("coding"))
        return Code(coding)

    def to_dict(self) -> dict:
        result: dict = {}
        result["coding"] = from_union([lambda x: from_list(
            lambda x: to_class(Coding, x), x), from_none], self.coding)
        return result


@dataclass
class Context:
    reference: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Context':
        assert isinstance(obj, dict)
        reference = from_union([from_str, from_none], obj.get("reference"))
        return Context(reference)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reference"] = from_union([from_str, from_none], self.reference)
        return result


@dataclass
class Identifier:
    value: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Identifier':
        assert isinstance(obj, dict)
        value = from_union([from_str, from_none], obj.get("value"))
        return Identifier(value)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_union([from_str, from_none], self.value)
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
class Subject:
    reference: Optional[str] = None
    display: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Subject':
        assert isinstance(obj, dict)
        reference = from_union([from_str, from_none], obj.get("reference"))
        display = from_union([from_str, from_none], obj.get("display"))
        return Subject(reference, display)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reference"] = from_union([from_str, from_none], self.reference)
        result["display"] = from_union([from_str, from_none], self.display)
        return result


@dataclass
class ValueQuantity:
    value: Optional[int] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ValueQuantity':
        assert isinstance(obj, dict)
        value = from_union([from_int, from_none], obj.get("value"))
        unit = from_union([from_str, from_none], obj.get("unit"))
        system = from_union([from_str, from_none], obj.get("system"))
        code = from_union([from_str, from_none], obj.get("code"))
        return ValueQuantity(value, unit, system, code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_union([from_int, from_none], self.value)
        result["unit"] = from_union([from_str, from_none], self.unit)
        result["system"] = from_union([from_str, from_none], self.system)
        result["code"] = from_union([from_str, from_none], self.code)
        return result


@dataclass
class PostObservation:
    resource_type: Optional[str] = None
    id: Optional[UUID] = None
    meta: Optional[Meta] = None
    identifier: Optional[List[Identifier]] = None
    status: Optional[str] = None
    code: Optional[Code] = None
    subject: Optional[Subject] = None
    context: Optional[Context] = None
    effective_date_time: Optional[datetime] = None
    issued: Optional[datetime] = None
    performer: Optional[List[Context]] = None
    value_quantity: Optional[ValueQuantity] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PostObservation':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [from_str, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union([Meta.from_dict, from_none], obj.get("meta"))
        identifier = from_union([lambda x: from_list(
            Identifier.from_dict, x), from_none], obj.get("identifier"))
        status = from_union([from_str, from_none], obj.get("status"))
        code = from_union([Code.from_dict, from_none], obj.get("code"))
        subject = from_union(
            [Subject.from_dict, from_none], obj.get("subject"))
        context = from_union(
            [Context.from_dict, from_none], obj.get("context"))
        effective_date_time = from_union(
            [from_datetime, from_none], obj.get("effectiveDateTime"))
        issued = from_union([from_datetime, from_none], obj.get("issued"))
        performer = from_union([lambda x: from_list(
            Context.from_dict, x), from_none], obj.get("performer"))
        value_quantity = from_union(
            [ValueQuantity.from_dict, from_none], obj.get("valueQuantity"))
        return PostObservation(resource_type, id, meta, identifier, status, code, subject, context, effective_date_time, issued, performer, value_quantity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [from_str, from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(Meta, x), from_none], self.meta)
        result["identifier"] = from_union([lambda x: from_list(
            lambda x: to_class(Identifier, x), x), from_none], self.identifier)
        result["status"] = from_union([from_str, from_none], self.status)
        result["code"] = from_union(
            [lambda x: to_class(Code, x), from_none], self.code)
        result["subject"] = from_union(
            [lambda x: to_class(Subject, x), from_none], self.subject)
        result["context"] = from_union(
            [lambda x: to_class(Context, x), from_none], self.context)
        result["effectiveDateTime"] = from_union(
            [lambda x: x.isoformat(), from_none], self.effective_date_time)
        result["issued"] = from_union(
            [lambda x: x.isoformat(), from_none], self.issued)
        result["performer"] = from_union([lambda x: from_list(
            lambda x: to_class(Context, x), x), from_none], self.performer)
        result["valueQuantity"] = from_union(
            [lambda x: to_class(ValueQuantity, x), from_none], self.value_quantity)
        return result


def post_observation_from_dict(s: Any) -> PostObservation:
    return PostObservation.from_dict(s)


def post_observation_to_dict(x: PostObservation) -> Any:
    return to_class(PostObservation, x)
