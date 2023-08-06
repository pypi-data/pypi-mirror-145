# Copyright (c) 2021 Petr Kracik

from ndef.record import Record, GlobalRecord
from io import BytesIO
import json

class CDFConfig(GlobalRecord):
    _type = 'cdf/cfg'

    def __init__(self, value=None):
        self._config = value

        if not self._config:
            self._config = {}
            self._config['v'] = 1
            self._config['key'] = "defaultkey"
            self._config['config'] = {}


    def __str__(self):
        return ("NDEF CDFConfig: Version: {} Key: {} Config: {}".format(self.version, self.key, self.config))
    

    def __repr__(self):
        return self.__str__()

    
    @property
    def version(self):
        return self._config['v']
    

    @property
    def key(self):
        return self._config['key']
    

    @property
    def config(self):
        return self._config['config']


    def _encode_payload(self):
        return json.dumps(self._config)


    @classmethod
    def _decode_payload(cls, octets, errors):
        stream = BytesIO(octets)
        data = stream.read()
        return cls(json.loads(data))


Record.register_type(CDFConfig)
