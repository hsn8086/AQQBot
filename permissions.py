import json
import os.path
from typing import Union


class Permissions:
    def __init__(self, fp):
        self.fp = fp
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf8') as f:
                self.p_json: dict = json.load(f)
        else:
            self.p_json = {'members': {}, 'groups': {}}

    def save(self):
        if not os.path.exists(self.fp):
            os.makedirs(os.path.split(self.fp)[0])
        with open(self.fp, 'w', encoding='utf8') as f:
            json.dump(self.p_json, f)

    def list_group(self):
        return self.p_json.keys()

    def group_create(self, name: str, permissions: dict, base: str):
        if name in self.p_json['groups']:
            raise KeyError(f'"{name}" already exists in the group')
        try:
            json.dumps(permissions)
            self.p_json['groups'][name]['permissions'] = permissions
        except:
            raise TypeError
        self.p_json['groups'][name]['base'] = base

    def group_del(self, name: str):
        if name in self.p_json['groups']:
            del self.p_json['groups'][name]

    def group_add_permissions(self, name: str, permissions: dict):
        try:
            json.dumps(permissions)
        except:
            raise TypeError
        for i in permissions:
            self.p_json['groups'][name]['permissions'][i] = permissions[i]

    def group_set_permissions(self, name: str, permissions: dict):
        try:
            json.dumps(permissions)
            self.p_json['groups'][name]['permissions'] = permissions
        except:
            raise TypeError

    def group_del_permission(self, name, permission: str):
        if permission in self.p_json['groups'][name]['permissions']:
            del self.p_json['groups'][name]['permissions'][permission]

    def group_del_permissions(self, name: str, permissions: Union[list, dict]):
        for i in permissions:
            self.group_del_permission(name, i)

    def group_list_permissions(self, name: str, include_base: bool = True):
        base = []
        if include_base:
            if 'base' in self.p_json['groups'][name]:
                base = self.group_list_permissions(self.p_json['groups'][name]['base'], True)

        return self.p_json['groups'][name]['permissions'].keys() + base

    def group_get_permissions(self, name: str, include_base: bool = True):
        base = {}
        if include_base:
            if 'base' in self.p_json['groups'][name]:
                base = self.group_get_permissions(self.p_json['groups'][name]['base'], True)

        return self.p_json['groups'][name]['permissions'] + base

    def group_set_base(self, name: str, base: str):
        if name in self.p_json['groups']:
            self.p_json['groups'][name]['base'] = base

    def group_query_permission(self, name: str, permission: str):
        if name in self.p_json['groups']:
            p_list = self.group_get_permissions(name, True)
            if permission in p_list:
                return p_list[permission]

    def member_create(self, name: str, permissions: dict, group: str):
        if name in self.p_json['members']:
            raise KeyError(f'"{name}" already exist')
        try:
            json.dumps(permissions)
            self.p_json['members'][name]['permissions'] = permissions
        except:
            raise TypeError
        self.p_json['members'][name]['group'] = group

    def member_add_permission(self, name: str, permission: str, value):
        self.p_json['members'][name]['permissions'][permission] = value

    def member_add_permissions(self, name: str, permissions: dict):
        json.dumps(permissions)
        for i in permissions:
            self.p_json['members'][name]['permissions'][i] = permissions[i]

    def member_list_permissions(self, name: str):
        addition = []
        if 'group' in self.p_json['members'][name]:
            addition = self.group_list_permissions(self.p_json['members'][name]['group'], True)
        return self.p_json['members'][name]['permissions'].keys() + addition

    def member_get_permissions(self, name: str):
        addition = {}
        if 'group' in self.p_json['members'][name]:
            addition = self.group_get_permissions(self.p_json['members'][name]['group'], True)
        return self.p_json['members'][name]['permissions'] + addition

    def member_query_permission(self, name: str, permission: str):
        if name in self.p_json['members']:
            p_list = self.member_get_permissions(name)
            if permission in p_list:
                return p_list[permission]
