import json


class Config:
    def __init__(self, conf_path):
        self.conf_path = conf_path
        self.conf = json.load(open(conf_path, 'r', encoding='utf-8'))

    def save_config(self):
        json.dump(self.conf, open(self.conf_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    def reload_config(self):
        self.conf = json.load(open(self.conf_path, 'r', encoding='utf-8'))

    def __getitem__(self, item):
        self.conf[item]

    def __setitem__(self, key, value):
        self.conf[key] = value
        self.save_config()

    def __delitem__(self, key):
        del self.conf[key]
        self.save_config()

    def __contains__(self, item):
        return item in self.conf

    def __iter__(self):
        return iter(self.conf)

    def __len__(self):
        return len(self.conf)
