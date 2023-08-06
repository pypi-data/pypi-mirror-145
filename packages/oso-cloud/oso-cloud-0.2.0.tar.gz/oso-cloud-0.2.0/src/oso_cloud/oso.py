import json
import os
from typing import Tuple

import requests


def extract_type_and_id(obj) -> Tuple[str, str]:
    if not hasattr(obj, "__dict__"):
        raise TypeError(f"Expected an instance of a class but received: {obj}")
    if not hasattr(obj, "id"):
        raise TypeError(f"Expected {obj} to have an 'id' attribute")
    return (obj.__class__.__name__, obj.id)


def to_params(role_or_relation, from_type, from_id, name, to_type, to_id):
    from_name = "resource" if role_or_relation == "role" else "from"
    to_name = "actor" if role_or_relation == "role" else "to"
    return {
        from_name + "_id": str(from_id),
        from_name + "_type": from_type,
        role_or_relation: name,
        to_name + "_id": str(to_id),
        to_name + "_type": to_type,
    }


class Oso:
    def __init__(self, url="https://cloud.osohq.com", api_key=None):
        self.url = url
        self.api_base = "api"
        if api_key:
            self.token = api_key
        else:
            raise ValueError("Must set an api_key")

    def _handle_result(self, result):
        if not result.ok:
            code, text = result.status_code, result.text
            msg = f"Got unexpected error from Oso Service: {code}\n{text}"
            raise Exception(msg)
        try:
            return result.json()
        except json.decoder.JSONDecodeError:
            return result.text

    def _do_post(self, url, json):
        headers = {"Authorization": f"Basic {self.token}"}
        return requests.post(url, json=json, headers=headers)

    def _do_get(self, url, params):
        headers = {"Authorization": f"Basic {self.token}"}
        return requests.get(url, params=params, headers=headers)

    def _do_delete(self, url, json):
        headers = {"Authorization": f"Basic {self.token}"}
        return requests.delete(url, json=json, headers=headers)

    def authorize(self, actor, action, resource):
        actor_type, actor_id = extract_type_and_id(actor)
        resource_type, resource_id = extract_type_and_id(resource)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize",
            json={
                "actor_type": actor_type,
                "actor_id": str(actor_id),
                "action": action,
                "resource_type": resource_type,
                "resource_id": str(resource_id),
            },
        )
        allowed = self._handle_result(result)["allowed"]
        return allowed

    def list(self, actor, action, resource_type):
        actor_type, actor_id = extract_type_and_id(actor)
        result = self._do_post(
            f"{self.url}/{self.api_base}/list",
            json={
                "actor_type": actor_type,
                "actor_id": str(actor_id),
                "action": action,
                "resource_type": resource_type,
            },
        )
        results = self._handle_result(result)["results"]
        return results

    def _add_role_or_relation(self, role_or_relation, from_, name, to):
        from_type, from_id = extract_type_and_id(from_)
        to_type, to_id = extract_type_and_id(to)
        params = to_params(role_or_relation, from_type, from_id, name, to_type, to_id)
        result = self._do_post(f"{self.url}/{self.api_base}/{role_or_relation}s", json=params)
        return self._handle_result(result)

    def _delete_role_or_relation(self, role_or_relation, from_, name, to):
        from_type, from_id = extract_type_and_id(from_)
        to_type, to_id = extract_type_and_id(to)
        params = to_params(role_or_relation, from_type, from_id, name, to_type, to_id)
        result = self._do_delete(f"{self.url}/{self.api_base}/{role_or_relation}s", json=params)
        return self._handle_result(result)

    def add_role(self, actor, role_name, resource):
        return self._add_role_or_relation("role", resource, role_name, actor)

    def add_relation(self, subject, name, object):
        return self._add_role_or_relation("relation", subject, name, object)

    def delete_role(self, actor, role_name, resource):
        return self._delete_role_or_relation("role", resource, role_name, actor)

    def delete_relation(self, subject, name, object):
        return self._delete_role_or_relation("relation", subject, name, object)

    def get_roles(self, resource=None, role=None, actor=None):
        params = {}
        if actor:
            actor_type, actor_id = extract_type_and_id(actor)
            params["actor_type"] = actor_type
            params["actor_id"] = actor_id
        if resource:
            resource_type, resource_id = extract_type_and_id(resource)
            params["resource_type"] = resource_type
            params["resource_id"] = resource_id
        if role:
            params["role"] = role
        result = self._do_get(f"{self.url}/{self.api_base}/roles", params=params)
        return self._handle_result(result)
