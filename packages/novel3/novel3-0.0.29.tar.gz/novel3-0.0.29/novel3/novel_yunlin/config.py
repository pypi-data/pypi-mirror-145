import json
from os.path import abspath


class Config:
    def __init__(self):
        self.novel_config = self.read_config()

    @classmethod
    def read_config(cls):
        with open('%s/../config/novel.json' % abspath(__file__), 'r', encoding='utf-8') as fp:
            return json.load(fp)

    @classmethod
    def save_config(cls, config):
        with open('%s/../config/novel.json' % abspath(__file__), 'w', encoding='utf-8') as fp:
            json.dump(config, fp, indent=4, ensure_ascii=False)

    @classmethod
    def set_domain(cls, domain):
        domain = domain.strip("/")
        config = cls.read_config()
        config['novel_domain'] = domain
        cls.save_config(config)

    @classmethod
    def set_novel_path(cls, novel_path):
        config = cls.read_config()
        config['novel_path'] = novel_path
        cls.save_config(config)
