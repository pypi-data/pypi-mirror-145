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
#     result = post_procedure_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


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


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Coding:
    code: Optional[int] = None
    system: Optional[str] = None
    display: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Coding':
        assert isinstance(obj, dict)
        code = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("code"))
        system = from_union([from_str, from_none], obj.get("system"))
        display = from_union([from_str, from_none], obj.get("display"))
        return Coding(code, system, display)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(
            x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.code)
        result["system"] = from_union([from_str, from_none], self.system)
        result["display"] = from_union([from_str, from_none], self.display)
        return result


@dataclass
class Code:
    text: Optional[int] = None
    coding: Optional[List[Coding]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Code':
        assert isinstance(obj, dict)
        text = from_union(
            [from_none, lambda x: int(from_str(x))], obj.get("text"))
        coding = from_union([lambda x: from_list(
            Coding.from_dict, x), from_none], obj.get("coding"))
        return Code(text, coding)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(
            x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.text)
        result["coding"] = from_union([lambda x: from_list(
            lambda x: to_class(Coding, x), x), from_none], self.coding)
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

    @staticmethod
    def from_dict(obj: Any) -> 'Subject':
        assert isinstance(obj, dict)
        reference = from_union([from_str, from_none], obj.get("reference"))
        return Subject(reference)

    def to_dict(self) -> dict:
        result: dict = {}
        result["reference"] = from_union([from_str, from_none], self.reference)
        return result


@dataclass
class PostProcedure:
    resource_type: Optional[str] = None
    id: Optional[UUID] = None
    meta: Optional[Meta] = None
    status: Optional[str] = None
    code: Optional[Code] = None
    subject: Optional[Subject] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PostProcedure':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [from_str, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union([Meta.from_dict, from_none], obj.get("meta"))
        status = from_union([from_str, from_none], obj.get("status"))
        code = from_union([Code.from_dict, from_none], obj.get("code"))
        subject = from_union(
            [Subject.from_dict, from_none], obj.get("subject"))
        return PostProcedure(resource_type, id, meta, status, code, subject)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [from_str, from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(Meta, x), from_none], self.meta)
        result["status"] = from_union([from_str, from_none], self.status)
        result["code"] = from_union(
            [lambda x: to_class(Code, x), from_none], self.code)
        result["subject"] = from_union(
            [lambda x: to_class(Subject, x), from_none], self.subject)
        return result


def post_procedure_from_dict(s: Any) -> PostProcedure:
    return PostProcedure.from_dict(s)


def post_procedure_to_dict(x: PostProcedure) -> Any:
    return to_class(PostProcedure, x)
