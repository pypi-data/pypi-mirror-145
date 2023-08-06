# guard_exception
    - guard all exception for swift run python

## install
    - pip install guard-exception


## example
```python
import guard_exception as ge

gg = ge.guard_exception()


def dividir(a, b):
    return a / b


print(gg.guardException(dividir, a=1, b=0))


# result cli
# {'data:': None, 'error': 'division by zero'}

```


## example on swift with PythonKit
```swift
import PythonKit
let hvac = Python.import("hvac")
let ge = Python.import("guard_exception")
let gg = ge.guard_exception()

let client = hvac.Client(url: "http://0.0.0.0:8200")

let user = "incorrect_user"
let params = Python.dict()
params["username"] = PythonObject(user)
params["password"] = PythonObject("incorrect_password")

print(gg.guardException(client.login, url: "v1/auth/userpass/login/\(user)", use_token: true, json: params))

// result: cli
//{'data:': None, 'error': 'invalid username or password, on post http://0.0.0.0:8200/v1/auth/userpass/login/incorrect_user'}
```