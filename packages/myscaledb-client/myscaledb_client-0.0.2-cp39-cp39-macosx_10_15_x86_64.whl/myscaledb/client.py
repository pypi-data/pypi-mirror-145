import asyncio
import csv
import json as json_
import sys
import warnings
import aiohttp
from enum import Enum
from types import TracebackType
from typing import Any, AsyncGenerator, Dict, List, Optional, Type

from myscaledb.exceptions import ClientError
from myscaledb.http_clients.abc import HttpClientABC
from myscaledb.records import FromJsonFabric, Record, RecordsFabric
from myscaledb.sql import sqlparse

# Optional cython extension:
try:
    from myscaledb._types import rows2ch, json2ch, py2ch
except ImportError:
    from myscaledb.types import rows2ch, json2ch, py2ch

import functools
import asyncio
from concurrent.futures import ThreadPoolExecutor


def force_async(fn):
    '''
    turns a sync function to async function using threads
    '''
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def force_sync(fn):
    '''
    turn an async function to sync function
    '''

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if asyncio.iscoroutine(res):
            return asyncio.get_event_loop().run_until_complete(res)
        return res

    return wrapper


def streamFile(file_name, offset):
    batch = []
    max_batch_size = 100000
    line = 0
    rows = ""

    csvfile = open(file_name, newline='')
    csvfile.seek(offset)
    if line == 1:
        for i in range(max_batch_size):
            row = csvfile.readline().rstrip('\r\n').replace('\"', '\'').encode()
            if len(row) != 0:
                row = b''.join([b'(', row, b')'])
                if i == 0:
                    print(row)
                batch.append(row)
            else:
                batch_str = b",".join(row for row in batch)
                csvfile.close()
                return batch_str, True, offset

    else:
        for i in range(max_batch_size):
            row = csvfile.readline()
            if i == 0:
                print(row)
            rows += row
        new_offset = csvfile.tell()
        csvfile.close()
        return rows, False, new_offset

    new_offset = csvfile.tell()
    csvfile.close()
    batch_str = b",".join(row for row in batch)
    return batch_str, False, new_offset


class QueryTypes(Enum):
    FETCH = 0
    INSERT = 1
    OTHER = 2


class Client:
    """ChClient connection class.

    Usage:

    .. code-block:: python

        async with aiohttp.ClientSession() as s:
            client = ChClient(s, compress_response=True)
            nums = await client.fetch("SELECT number FROM system.numbers LIMIT 100")

    :param aiohttp.ClientSession session:
        aiohttp client session. Please, use one session
        and one ChClient for all connections in your app.

    :param str url:
        Clickhouse server url. Need full path, like "http://localhost:8123/".

    :param str user:
        User name for authorization.

    :param str password:
        Password for authorization.

    :param str database:
        Database name.

    :param bool compress_response:
        Pass True if you want Clickhouse to compress its responses with gzip.
        They will be decompressed automatically. But overall it will be slightly slower.

    :param **settings:
        Any settings from https://clickhouse.yandex/docs/en/operations/settings
    """

    __slots__ = (
        "_session",
        "url",
        "params",
        "_json",
        "_http_client",
        "stream_batch_size",
    )

    @force_sync
    async def generate_http_session(self):
        session = aiohttp.ClientSession()
        return session

    def __init__(
        self,
        session=None,
        url: str = "http://localhost:8123/",
        user: str = None,
        password: str = None,
        database: str = "default",
        compress_response: bool = False,
        stream_batch_size: int = 1000000,
        json=json_,  # type: ignore
        **settings,
    ):
        if not session:
            session = self.generate_http_session()
        _http_client = HttpClientABC.choose_http_client(session)
        self._http_client = _http_client(session)
        self.url = url
        self.params = {}
        if user:
            self.params["user"] = user
        if password:
            self.params["password"] = password
        if database:
            self.params["database"] = database
        if compress_response:
            self.params["enable_http_compression"] = 1
        self._json = json
        self.params.update(settings)
        self.stream_batch_size = stream_batch_size

    async def __aenter__(self) -> 'ChClient':
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close_async()

    async def close_async(self) -> None:
        """Close the session"""
        await self._http_client.close()

    def close(self) -> None:
        @force_sync
        async def sync_run():
            await self.close_async()

        return sync_run()

    async def is_alive_async(self) -> bool:
        """Checks if connection is Ok.

        Usage:

        .. code-block:: python

            assert await client.is_alive()

        :return: True if connection Ok. False instead.
        """
        try:
            await self._http_client.get(
                url=self.url, params={**self.params, "query": "SELECT 1"}
            )
        except ClientError:
            return False
        return True

    def is_alive(self) -> bool:
        @force_sync
        async def sync_run():
            return await self.is_alive_async()

        return sync_run()

    @staticmethod
    def _prepare_query_params(params: Optional[Dict[str, Any]] = None):
        if params is None:
            return {}
        if not isinstance(params, dict):
            raise TypeError('Query params must be a Dict[str, Any]')
        prepared_query_params = {}
        for key, value in params.items():
            prepared_query_params[key] = py2ch(value).decode('utf-8')
        return prepared_query_params

    async def _execute(
        self,
        query: str,
        *args,
        json: bool = False,
        query_params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> AsyncGenerator[Record, None]:
        query_params = self._prepare_query_params(query_params)
        if query_params:
            query = query.format(**query_params)
        need_fetch, is_json, is_csv, statement_type = self._parse_squery(query)

        if not is_json and json:
            query += " FORMAT JSONEachRow"
            is_json = True

        if not is_json and need_fetch:
            query += " FORMAT TSVWithNamesAndTypes"

        if args:
            if statement_type != 'INSERT':
                raise ClientError(
                    "It is possible to pass arguments only for INSERT queries"
                )
            params = {**self.params, "query": query}

            if is_json:
                data = json2ch(*args, dumps=self._json.dumps)
            elif is_csv:
                # we'll fill the data incrementally from file
                if len(args) > 1:
                    raise ClientError("only one argument is accepted in file read mode")
                data = []
            else:
                data = rows2ch(*args)
        else:
            params = {**self.params}
            data = query.encode()

        if query_id is not None:
            params["query_id"] = query_id

        if is_csv:
            sent = False
            rows_read = 0
            retry = 0
            max_batch_size = self.stream_batch_size
            csvfile = open(args[0], newline='')
            while True:
                rows = "".join(csvfile.readlines(max_batch_size))
                if len(rows) == 0:
                    csvfile.close()
                    break
                rows_read += max_batch_size
                while not sent:
                    if retry >= 3:
                        print("pipe breaks too many time, existing")
                        sys.exit(1)
                    try:
                        await self._http_client.post_no_return(
                            url=self.url, params=params, data=rows
                        )
                        sent = True
                    except aiohttp.ClientOSError as e:
                        if e.errno == 32:
                            print("broken pipe, retrying")
                            retry += 1
                        else:
                            raise e
                retry = 0
                sent = False

        elif need_fetch:
            response = self._http_client.post_return_lines(
                url=self.url, params=params, data=data
            )
            if is_json:
                rf = FromJsonFabric(loads=self._json.loads)
                async for line in response:
                    yield rf.new(line)
            else:
                rf = RecordsFabric(
                    names=await response.__anext__(),
                    tps=await response.__anext__(),
                    convert=decode,
                )
                async for line in response:
                    yield rf.new(line)
        else:
            await self._http_client.post_no_return(
                url=self.url, params=params, data=data
            )

    async def execute_async(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
    ) -> None:
        """Execute query. Returns None.

        :param str query: Clickhouse query string.
        :param args: Arguments for insert queries.
        :param bool json: Execute query in JSONEachRow mode.
        :param Optional[Dict[str, Any]] params: Params to escape inside query string.
        :param str query_id: Clickhouse query_id.

        Usage:

        .. code-block:: python

            await client.execute(
                "CREATE TABLE t (a UInt8, b Tuple(Date, Nullable(Float32))) ENGINE = Memory"
            )
            await client.execute(
                "INSERT INTO t VALUES",
                (1, (dt.date(2018, 9, 7), None)),
                (2, (dt.date(2018, 9, 8), 3.14)),
            )
            await client.execute(
                "INSERT INTO {table_name} VALUES",
                (1, (dt.date(2018, 9, 7), None)),
                (2, (dt.date(2018, 9, 8), 3.14)),
                params={"table_name": "t"}
            )

        :return: Nothing.
        """
        async for _ in self._execute(
            query, *args, json=json, query_params=params, query_id=query_id
        ):
            return None

    def execute(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
    ):
        @force_sync
        async def sync_run(
            query: str,
            *args,
            json: bool = False,
            params: Optional[Dict[str, Any]] = None,
            query_id: str = None,
        ):
            await self.execute_async(
                query, *args, json=json, params=params, query_id=query_id
            )

        sync_run(query, *args, json=json, params=params, query_id=query_id)

    async def fetch_async(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> List[Record]:
        """Execute query and fetch all rows from query result at once in a list.

        :param query: Clickhouse query string.
        :param bool json: Execute query in JSONEachRow mode.
        :param Optional[Dict[str, Any]] params: Params to escape inside query string.
        :param str query_id: Clickhouse query_id.
        :param decode: Decode to python types. If False, returns bytes for each field instead.

        Usage:

        .. code-block:: python

            all_rows = await client.fetch("SELECT * FROM t")

        :return: All rows from query.
        """
        return [
            row
            async for row in self._execute(
                query,
                *args,
                json=json,
                query_params=params,
                query_id=query_id,
                decode=decode,
            )
        ]

    def fetch(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> List[Record]:
        @force_sync
        async def sync_run(
            query: str,
            *args,
            json: bool = False,
            params: Optional[Dict[str, Any]] = None,
            query_id: str = None,
            decode: bool = True,
        ) -> List[Record]:
            return await self.fetch_async(
                query, *args, json=json, params=params, query_id=query_id, decode=decode
            )

        return sync_run(
            query, *args, json=json, params=params, query_id=query_id, decode=decode
        )

    async def fetchrow(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> Optional[Record]:
        """Execute query and fetch first row from query result or None.

        :param query: Clickhouse query string.
        :param bool json: Execute query in JSONEachRow mode.
        :param Optional[Dict[str, Any]] params: Params to escape inside query string.
        :param str query_id: Clickhouse query_id.
        :param decode: Decode to python types. If False, returns bytes for each field instead.

        Usage:

        .. code-block:: python

            row = await client.fetchrow("SELECT * FROM t WHERE a=1")
            assert row[0] == 1
            assert row["b"] == (dt.date(2018, 9, 7), None)

        :return: First row from query or None if there no results.
        """
        async for row in self._execute(
            query,
            *args,
            json=json,
            query_params=params,
            query_id=query_id,
            decode=decode,
        ):
            return row
        return None

    async def fetchone(self, query: str, *args) -> Optional[Record]:
        """Deprecated. Use ``fetchrow`` method instead"""
        warnings.warn(
            "'fetchone' method is deprecated. Use 'fetchrow' method instead",
            PendingDeprecationWarning,
        )
        return await self.fetchrow(query, *args)

    async def fetchval(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> Any:
        """Execute query and fetch first value of the first row from query result or None.

        :param query: Clickhouse query string.
        :param bool json: Execute query in JSONEachRow mode.
        :param Optional[Dict[str, Any]] params: Params to escape inside query string.
        :param str query_id: Clickhouse query_id.
        :param decode: Decode to python types. If False, returns bytes for each field instead.

        Usage:

        .. code-block:: python

            val = await client.fetchval("SELECT b FROM t WHERE a=2")
            assert val == (dt.date(2018, 9, 8), 3.14)

        :return: First value of the first row or None if there no results.
        """
        async for row in self._execute(
            query,
            *args,
            json=json,
            query_params=params,
            query_id=query_id,
            decode=decode,
        ):
            if row:
                return row[0]
        return None

    async def iterate(
        self,
        query: str,
        *args,
        json: bool = False,
        params: Optional[Dict[str, Any]] = None,
        query_id: str = None,
        decode: bool = True,
    ) -> AsyncGenerator[Record, None]:
        """Async generator by all rows from query result.

        :param str query: Clickhouse query string.
        :param bool json: Execute query in JSONEachRow mode.
        :param Optional[Dict[str, Any]] params: Params to escape inside query string.
        :param str query_id: Clickhouse query_id.
        :param decode: Decode to python types. If False, returns bytes for each field instead.

        Usage:

        .. code-block:: python

            async for row in client.iterate(
                "SELECT number, number*2 FROM system.numbers LIMIT 10000"
            ):
                assert row[0] * 2 == row[1]

            async for row in client.iterate(
                "SELECT number, number*2 FROM system.numbers LIMIT {numbers_limit}",
                params={"numbers_limit": 10000}
            ):
                assert row[0] * 2 == row[1]

        :return: Rows one by one.
        """
        async for row in self._execute(
            query,
            *args,
            json=json,
            query_params=params,
            query_id=query_id,
            decode=decode,
        ):
            yield row

    async def cursor(self, query: str, *args) -> AsyncGenerator[Record, None]:
        """Deprecated. Use ``iterate`` method instead"""
        warnings.warn(
            "'cursor' method is deprecated. Use 'iterate' method instead",
            PendingDeprecationWarning,
        )
        async for row in self.iterate(query, *args):
            yield row

    @staticmethod
    def _parse_squery(query):
        statement = sqlparse.parse(query)[0]
        statement_type = statement.get_type()
        if statement_type in ('SELECT', 'SHOW', 'DESCRIBE', 'EXISTS'):
            need_fetch = True
        else:
            need_fetch = False

        fmt = statement.token_matching(
            (lambda tk: tk.match(sqlparse.tokens.Keyword, 'FORMAT'),), 0
        )
        if fmt:
            is_json = statement.token_matching(
                (lambda tk: tk.match(None, ['JSONEachRow']),),
                statement.token_index(fmt) + 1,
            )
        else:
            is_json = False

        fmt2 = statement.token_matching(
            (lambda tk: tk.match(sqlparse.tokens.Keyword, 'FORMAT'),), 0
        )
        if fmt2:
            is_csv = statement.token_matching(
                (lambda tk: tk.match(None, ['CSV']),),
                statement.token_index(fmt2) + 1,
            )
        else:
            is_csv = False

        return need_fetch, is_json, is_csv, statement_type
