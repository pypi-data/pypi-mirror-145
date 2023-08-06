from typing import Optional
from pydevmgr_core import BaseRpc



class BaseSerialRpc(BaseRpc):
    def __init__(self, key=None, config=None, com=None, **kwargs): 
        # parse the config and com object 
        super().__init__(key=key, config=config, **kwargs)
        self._com = com 
    
    @property
    def sid(self):
        self._com.port
    
    @classmethod
    def new_args(cls, parent, config):
        d = super().new_args(parent, config)
        d.update(com=parent.com)
        return d
        
    def fcall(self, *args, **kwargs):
        raise NotImplementedError('fcall')
        
        
