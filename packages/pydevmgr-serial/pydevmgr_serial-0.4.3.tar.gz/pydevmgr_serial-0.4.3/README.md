An pydevmgr_core extension for serial communication 



Sources are [here](https://github.com/efisoft-elt/pydevmgr_serial) 

Doc to comme


# Install

```bash
> pip install pydevmgr_serial 
```

# Basic Usage

Bellow is an exemple of implementation of a node that check a value from a Tesla Sensor. 
An extra configuration argument is added and the fget method is implemented. 

```python 
from pydevmgr_serial import BaseSerialNode, SerialCom
import time

class TesaNodeConfig(BaseSerialNode.Config):
    type : 'Tesa'
    delay: float = 0.1 
    
class TesaNode(BaseSerialNode):
    Config = TesaNodeConfig
    def fget(self):
        self.com.serial.write(b'?\r')
        time.sleep(self.config.delay)
        sval = self.com.serial.read(20)
        val = float(sval)
        return val
```

```python 
# build a standalone node 
tesa_com = SerialCom(port='COM1', baudrate=9600)
tesa = TesaNode(com=tesa_com)
try:
    tesa_com.connect()
    print( "Position is ", tesa.get() )
finally:
    tesa_com.disconnect()
```

One can include the node in device

```python 
from pydevmgr_serial import BaseSerialDevice
from pydevmgr_core import NodeAlias



class Tesa(BaseSerialDevice):    
    raw_pos = TesaNode.Prop('raw_pos')
    
    @NodeAlias.prop('scaled_pos',['raw_pos'])
    def scaled_pos(self, raw_pos):
        return 10 + 1.3 * raw_pos    
```

```python 
tesa = Tesa('tesa', com={'port':'COM1'})
tesa.connect()
tesa.scaled_pos.get()
```



