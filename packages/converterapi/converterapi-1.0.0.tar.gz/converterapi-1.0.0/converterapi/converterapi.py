# please install multipledispatch 0.6.0
from socket import timeout
import requests
from urllib.parse import urljoin
import json
import polling2
from .data import Task, Version, Option

class Error():
    def __init__(self, res = None, proc_msg = None):
        self.status_code = None
        self.converter_msg = None
        self.program_msg = proc_msg
        self.res = res

        if self.res is not None:
            self.status_code = res.status_code
            self.converter_msg = res.content.decode('utf-8')
            print(self.converter_msg)
    
    @property
    def status_msg(self):
        # 4xx error -> client error, 5xx error -> server error
        if self.status_code == 400:
            return f"Bad Request({self.status_code})! Try again."
        elif self.status_code == 401:
            return f"Unauthorized({self.status_code})! Try again."
        elif self.status_code == 403:
            return f"Forbidden({self.status_code})! Try again."
        elif self.status_code == 404:
            return f"Not Found({self.status_code})! Try again."
        elif self.status_code == 500:
            return f"Internal Server Error({self.status_code})! - {self.converter_msg}"
        else:
            return f"Unknown Error. Original error message - {self.converter_msg}"

class ConverterServer():
    def __init__(self, addr, port, network_request_time_out=5):
        self.address = f"http://{addr}:{port}/"
        self.timeout = network_request_time_out

    def _check_status(self, res):
        if res.status_code >= 400: # More than 400 is seen as an issue on the device farm side.
            return False
        else:
            return True

    def _poll(self, add_str, method, files=None, data=None, params=None, headers=None):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = None
        try:
            if method == "get":
                res = polling2.poll(
                    lambda: requests.get(
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=data,
                        params=params,
                        headers=headers
                    ),
                    check_success = self._check_status,
                    step=5,
                    timeout=self.timeout)
            elif method == "post":
                res = polling2.poll(
                    lambda: requests.post(
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=data,
                        params=params,
                        headers=headers
                    ),
                    check_success = self._check_status,
                    step=5,
                    timeout=self.timeout)
            elif method == "delete":
                res = polling2.poll(
                    lambda: requests.delete(
                        url=urljoin(self.address, add_str),
                        files=files,
                        data=data,
                        params=params,
                        headers=headers
                    ),
                    check_success = self._check_status,
                    step=5,
                    timeout=self.timeout)
        except polling2.TimeoutException as e:
            return res, Error(e.last)
        return res, None
    
    def get_task(self, uuid:str = None, compile_type:str = None, status:str = None):
        params = {
            "uuid": uuid,
            "compile_type": compile_type,
            "status": status
        }
        res, error = self._poll(add_str=f"api/v1/task", method="get", params=params)
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        tasks = []
        [tasks.append(Task(res["data"][i])) for i in range(0, len(res["data"]))]
        # return lists, None
        return tasks, None

    def create_task(self, data: dict):
        res, error = self._poll(add_str=f"api/v1/task", method="post", data=json.dumps(data))
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        return Task(res), None

    def delete_task(self, task_uuid: str):
        data = {
            "uuid": task_uuid
        }
        res, error = self._poll(add_str=f"api/v1/task", method="delete", data=json.dumps(data))
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        return res, None

    def get_support_compiler(self):
        res, error = self._poll(add_str=f"api/v1/compiler", method="get")
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        compilers = []
        [compilers.append(res["support_compilers"][i]) for i in range(0, len(res["support_compilers"]))]
        return compilers, None

    def get_compiler_versions(self, compiler:str):
        params = {
            "compiler": compiler
        }
        res, error = self._poll(add_str=f"api/v1/compiler/version", method="get", params=params)
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        return Version(res), None

    def get_support_board(self, compiler:str):
        params = {
            "compiler": compiler
        }
        res, error = self._poll(add_str=f"api/v1/compiler/board", method="get", params=params)
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        boards = []
        [boards.append(res["support_board"][i]) for i in range(0, len(res["support_board"]))]
        return boards, None
    
    def get_support_option(self, compiler:str):
        params = {
            "compiler": compiler
        }
        res, error = self._poll(add_str=f"api/v1/compiler/option", method="get", params=params)
        if error is not None:
            return None, error
        res = json.loads(res.content.decode('utf-8'))
        return Option(res), None