# Copyright 2022 Belmont Technology
from unittest import result
import requests
import os
import uuid
import codecs
import dill
import json
import time
import logging

from dotenv import load_dotenv
from rich import pretty
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)

pretty.install()
load_dotenv()

daisi_base_url = "https://app.daisi.io"
daisi_base_route = "/pebble-api/pebbles"
daisi_new_route = "/pebble-api/daisies"


def _load_dill_string(s):  # pragma: no cover
    return dill.loads(codecs.decode(s.encode(), "base64"))


def _get_dill_string(obj):  # pragma: no cover
    return codecs.encode(dill.dumps(obj, protocol=5), "base64").decode()


def _is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


class DaisiResponseNotReady(Exception):
    def __init__(self, status):
        self.status = status


class DaisiExecution:
    def __init__(self, daisi, endpoint: str, arguments: dict):
        self.id = None
        self.daisi = daisi
        self.endpoint = endpoint
        self.arguments = arguments
        self.last_status = "NOT_STARTED"
        self._result = None
        self.value_fetched = False

        # Prepare the arguments
        parsed_args = self._pickle_hidden(self.arguments)
        parsed_args["_endpoint"] = self.endpoint

        self.parsed_args = parsed_args

    def _store_pickle(self, data):
        my_args = {"data": data}

        # Call the specified Daisi compute
        r = self.daisi.session.post(f"{self.daisi.base_url}/pickle", json=my_args)

        # Return the result
        return r.content.decode()

    def _pickle_hidden(self, args):
        final_args = {}
        for k, v in args.items():
            # First check if it's a DaisiExecution object
            if type(v) == DaisiExecution:
                # Grab the last result
                v = v._result["outputs"][-1]["data"]

            if not _is_jsonable(v):
                x = self._store_pickle(_get_dill_string(v))
                final_args[k] = "lookup:" + x
            else:
                final_args[k] = v

        return final_args

    def get_status(self):
        if self.last_status not in ["FINISHED", "FAILED"]:
            r = self.daisi.session.get(
                f"{self.daisi.base_url}/{self.daisi.id}/executions/{self.id}/status"
            )
            self.last_status = r.json()

        return self.last_status

    def get_logs(self, limit: int = None):
        limit_param = {"limit": limit} if limit is not None else None

        r = self.daisi.session.get(
            f"{self.daisi.base_url}/{self.daisi.id}/executions/{self.id}/logs",
            params=limit_param,
        )

        res = r.json()

        return res

    def _unpickle_hidden(self):
        final_outputs = []
        for item in self._result["outputs"]:
            if item["type"] in ["console-log", "data-grid"]:
                continue

            if type(item["data"]) == str and item["data"].startswith("lookup:"):
                # Get the binary data
                l_split = item["data"].split("lookup:")

                r = self.daisi.session.get(
                    f"{self.daisi.base_url}/pickle", params={"lookup": l_split[1]}
                )
                item["data"] = _load_dill_string(r.content.decode())

            final_outputs.append(item)

        self._result["outputs"] = final_outputs

    @property
    def value(self):
        return self.fetch_result()

    def fetch_result(self):
        if not self.value_fetched:
            if self.get_status() in ["FINISHED", "FAILED"]:
                r = self.daisi.session.get(
                    f"{self.daisi.base_url}/{self.daisi.id}/executions/{self.id}/results"
                )
                self._result = r.json()
                self._unpickle_hidden()

                if self._result["outputs"][0].get("label") == "ERROR":
                    self.last_status = "FAILED"

                    error_id = self._result["outputs"][0]["data"]["id"]

                    r = self.daisi.session.get(f"{self.daisi.base_url}/outputs/html/{error_id}")
                    self._result["outputs"][0]["data"] = r.content.decode()

                self.value_fetched = True
            else:
                raise DaisiResponseNotReady(self.last_status)

        if len(self._result["outputs"]) > 1:
            return [x["data"] for x in self._result["outputs"]]
        else:
            return self._result["outputs"][0]["data"]


class Daisi:
    """
    A utility to assist in developing Daisis for the Daisi platform.

    A tool for creating, validating, publishing, and updating daisis.

    :param daisi_id: A daisi name or UUID
    :param base_url: The default URL to use for connecting to the daisi
    :param access_token: access token for authorizing to the platform
    """

    def __init__(
        self, daisi_id: str, *, base_url: str = daisi_base_url, access_token: str = ""
    ):
        """
        Daisi constructor method.

        :param daisi_id:  A Daisi name or UUID

        :raises ValueError: DaisiID Not Found (Non-200 response)
        """
        self.id = None
        self.name = None
        self.description = None
        self.endpoints = None
        self.base_url = base_url + daisi_base_route
        self.session = requests.Session()
        access_token = access_token or os.getenv("DAISI_ACCESS_TOKEN", "")
        self.new_url = base_url + daisi_new_route

        if access_token:
            self.session.headers.update({"Authorization": f"token {access_token}"})

        # Check if it's a valid uuid:
        try:
            check_uuid = uuid.UUID(daisi_id) is not None
        except Exception as e:
            check_uuid = False

        if check_uuid:
            r = self.session.get(f"{self.base_url}/{daisi_id}")
            if not r.ok:
                raise ValueError("The specified Daisi ID could not be found.")
            else:
                logger.info(f"Found existing Daisi: {r.json()['name']}")

                self.name = r.json()["name"]
                self.id = daisi_id
        else:
            logger.info(f"Calling {self.new_url}/search with query {daisi_id}")
            r = self.session.get(
                f"{self.new_url}/search",
                params={"term[]": [daisi_id], "pageSize": 1, "page": 1},
            )
            result = r.json()

            if result and result["success"] and result["data"]["data"]:
                self.name = daisi_id
                daisi_id = result["data"]["data"][0]["id"]
                logger.info(f"Found existing Daisi: {daisi_id}")
                self.id = daisi_id
            else:
                # TODO: Handle git repo connection here
                raise ValueError("That daisi could not be found.")

        # Call the specified Daisi endpoints
        r = self.session.get(f"{self.base_url}/{self.id}/endpoints")

        _endpoints = r.json() if r.ok else {}

        self.endpoints = {x["name"]: x["schema"] for x in _endpoints}
        functionlist = list(self.endpoints.keys())
        for f in functionlist:
            # Sync / blocking version
            self.__setattr__(
                f,
                (
                    lambda f: (lambda _, *a, **kwa: _._run(f, True, a, kwa)).__get__(
                        self
                    )
                )(f),
            )

            # Async / non-blocking version
            self.__setattr__(
                f + "_",
                (
                    lambda f: (lambda _, *a, **kwa: _._run(f, False, a, kwa)).__get__(
                        self
                    )
                )(f),
            )

    def dispatch(self, _func="compute", *args, **kwargs):
        # call as daisi.dispatch("functionname", arg1, arg2, p3=arg3)
        # Possible conflict if the function takes a keyword argument also named "_func".
        # Could rename the param to "__", or just call using "_run()"
        return self._run(_func, False, args, kwargs)

    def _run(self, _func="compute", wait_for_completion=True, args:tuple=(), kwargs=None):
        kwargs = kwargs if kwargs is not None else {}
        param_names = [p["id"] for p in self.endpoints[_func]]
        kwargs.update(zip(param_names, args))

        # Grab a new DaisiExecution
        daisi_execution = DaisiExecution(daisi=self, endpoint=_func, arguments=kwargs)

        logger.info(
            "[bold blue]=== BEGINNING DAISI EXECUTION WITH PARAMETERS ===[/bold blue]"
        )
        logger.info(daisi_execution.parsed_args)

        r = self.session.post(
            f"{self.base_url}/{self.id}/executions", json=daisi_execution.parsed_args
        )

        if not r.ok:
            daisi_execution.last_status = "FAILED"
            logger.error("[bold red]=== DAISI EXECUTION FAILED ===[bold red]")

            return daisi_execution

        # Store the id
        daisi_execution.id = r.json()["id"]

        logger.info(
            f"[bold blue]=== DAISI EXECUTION STARTED: [/bold blue]{daisi_execution.id}[bold blue]===[/bold blue]"
        )

        if wait_for_completion:
            logger.info("[bold blue]=== DAISI EXECUTION LIVE LOGS ===[/bold blue]")

            while daisi_execution.get_status() not in ["FINISHED", "FAILED"]:
                log = daisi_execution.get_logs(limit=1)
                if log:
                    logger.info(f"[yellow]{log[0]}[/yellow]")

                time.sleep(0.25)

            logger.info("[bold green]=== DAISI EXECUTION FINISHED ===[/bold green]")
            logger.info("[bold blue]=== DAISI EXECUTION FINAL LOGS ===[/bold blue]")
            logger.info(daisi_execution.get_logs())
            # logger.info("\n")
            # logger.info("[bold blue]=== DAISI EXECUTION FINAL RESULTS ===[/bold blue]")
            # logger.info(daisi_execution.fetch_result())

        return daisi_execution

    @staticmethod
    def get_daisies(base_url: str = daisi_base_url, access_token: str = ""):
        """
        Queries Daisi platform for a list of all current daisis.

        :return: List of daisis available on the Daisi platform.
        :rtype list
        """

        access_token = access_token or os.getenv("DAISI_ACCESS_TOKEN") or ""
        headers = {"Authorization": f"token {access_token}"} if access_token else None

        r = requests.get(
            f"{base_url}{daisi_new_route}",
            params={"pageSize": 10000, "page": 1},
            headers=headers,
        )
        result = r.json()

        return_list = []
        for daisi in result["data"][0]["data"]:
            return_list.append(
                {
                    "id": daisi["id"],
                    "name": daisi["name"],
                    "description": daisi["description"],
                }
            )

        final_return = sorted(return_list, key=lambda x: x["name"])

        return final_return
