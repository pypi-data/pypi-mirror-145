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
#     result = get_procedure_from_dict(json.loads(json_string))

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
class Resource:
    resource_type: Optional[str] = None
    id: Optional[UUID] = None
    meta: Optional[ResourceMeta] = None
    status: Optional[str] = None
    code: Optional[Code] = None
    subject: Optional[Subject] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Resource':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [from_str, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union([ResourceMeta.from_dict, from_none], obj.get("meta"))
        status = from_union([from_str, from_none], obj.get("status"))
        code = from_union([Code.from_dict, from_none], obj.get("code"))
        subject = from_union(
            [Subject.from_dict, from_none], obj.get("subject"))
        return Resource(resource_type, id, meta, status, code, subject)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [from_str, from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(ResourceMeta, x), from_none], self.meta)
        result["status"] = from_union([from_str, from_none], self.status)
        result["code"] = from_union(
            [lambda x: to_class(Code, x), from_none], self.code)
        result["subject"] = from_union(
            [lambda x: to_class(Subject, x), from_none], self.subject)
        return result


@dataclass
class Search:
    mode: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Search':
        assert isinstance(obj, dict)
        mode = from_union([from_str, from_none], obj.get("mode"))
        return Search(mode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["mode"] = from_union([from_str, from_none], self.mode)
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
class GetProcedureMeta:
    last_updated: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GetProcedureMeta':
        assert isinstance(obj, dict)
        last_updated = from_union(
            [from_datetime, from_none], obj.get("lastUpdated"))
        return GetProcedureMeta(last_updated)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lastUpdated"] = from_union(
            [lambda x: x.isoformat(), from_none], self.last_updated)
        return result


@dataclass
class GetProcedure:
    resource_type: Optional[str] = None
    id: Optional[UUID] = None
    meta: Optional[GetProcedureMeta] = None
    type: Optional[str] = None
    link: Optional[List[Link]] = None
    entry: Optional[List[Entry]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'GetProcedure':
        assert isinstance(obj, dict)
        resource_type = from_union(
            [from_str, from_none], obj.get("resourceType"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        meta = from_union([GetProcedureMeta.from_dict,
                          from_none], obj.get("meta"))
        type = from_union([from_str, from_none], obj.get("type"))
        link = from_union([lambda x: from_list(
            Link.from_dict, x), from_none], obj.get("link"))
        entry = from_union([lambda x: from_list(
            Entry.from_dict, x), from_none], obj.get("entry"))
        return GetProcedure(resource_type, id, meta, type, link, entry)

    def to_dict(self) -> dict:
        result: dict = {}
        result["resourceType"] = from_union(
            [from_str, from_none], self.resource_type)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        result["meta"] = from_union(
            [lambda x: to_class(GetProcedureMeta, x), from_none], self.meta)
        result["type"] = from_union([from_str, from_none], self.type)
        result["link"] = from_union([lambda x: from_list(
            lambda x: to_class(Link, x), x), from_none], self.link)
        result["entry"] = from_union([lambda x: from_list(
            lambda x: to_class(Entry, x), x), from_none], self.entry)
        return result


def get_procedure_from_dict(s: Any) -> GetProcedure:
    return GetProcedure.from_dict(s)


def get_procedure_to_dict(x: GetProcedure) -> Any:
    return to_class(GetProcedure, x)
