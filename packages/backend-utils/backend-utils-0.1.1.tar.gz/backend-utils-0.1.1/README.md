# backend-utils
utils for fastapi backend


## Documentation

### Tools

* `Singleton` - metaclass to make singletons
```python
from backend_utils.tools import Singleton

class A(metaclass=Singleton):
    pass

print(id(A()) == id(A())) # True
```

* `StrEnum` - subclasses that create variants using `auto()` will have values equal to their names
```python
from enum import auto

from backend_utils.tools import StrEnum

class Bit(StrEnum):
    one = auto()
    two = auto()

print(Bit.one.value) # 'one'
print(Bit.two.value) # 'two'
```

### Server

* `Router`, `compile_routers`, `register_routers` - build routers 
for fastapi app

```python
from fastapi import FastAPI, APIRouter

from backend_utils.server import (
    Router, compile_routers, register_routers
)
router = APIRouter()

routers = [
    Router(router=router, tags=['Users'], prefix='/users'),
]


compiled_routers = compile_routers(
    routers=routers,
    root_prefix='/api/v1'
)

app = FastAPI()
register_routers(
    app=app,
    routers=[*compiled_routers]
)
```
This code will compile routers:
`/api/v1/users/*`
