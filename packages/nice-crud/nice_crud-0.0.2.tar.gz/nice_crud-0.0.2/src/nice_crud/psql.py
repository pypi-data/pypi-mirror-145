import typing as t

import psycopg2

from . import exceptions


class PostgresCrud:
    __create_table_col_types = t.Union[
        t.Text,
        t.Dict[str, str],
        t.List[t.List[str]],
        t.List[t.Dict[str, str]],
        t.List[t.Tuple[str, str]],
        t.Tuple[t.Tuple[str]],
        t.Tuple[t.Dict[str, str]],
        t.Tuple[t.List[str]],
    ]

    __create_index_col_types = t.Union[
        t.Text,
        t.Dict[t.Text, t.Text],
        t.List[t.Union[t.Tuple[str, str], t.List, t.Text]],
        t.Tuple[t.Union[t.Tuple[str, str], t.List, t.Text]],
    ]

    __INDEX_TYPES = ['btree', 'hash', 'gist', 'gin', 'spgist', 'brin', 'b-tree', 'sp-gist']

    def __init__(
            self, dbname: str, user: str, password: str, host: str, port: int, close_conn: bool = False
    ):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port

        self._conn = None
        self._close_conn = close_conn

    def _db_data_to_dict(self) -> t.Dict:
        return {
            'db_name': self._dbname,
            'db_user': self._user,
            'db_password': self._password,
            'db_host': self._host,
            'db_port': self._port
        }

    def _connect(self):
        if self._conn is None:
            try:
                self._conn = psycopg2.connect(
                    dbname=self._dbname,
                    user=self._user,
                    password=self._password,
                    host=self._host,
                    port=self._port
                )
                return self._conn
            except Exception as e:
                raise exceptions.ConnectionException(
                    func_name='connect', message=f'Connection Error: {e}', db_data=self._db_data_to_dict()
                )

        return self._conn

    def _close(self):
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception as e:
                raise exceptions.ConnectionException(
                    func_name='close', message=f'Connection Error: {e}', db_data=self._db_data_to_dict()
                )
        return True

    def _execute(self, func_name: str, sql: str, type_: str, func_params, **kwargs):
        __locals__ = locals()
        __locals__.pop('self')

        conn = self._connect()
        cur = conn.cursor()

        try:
            cur.execute(sql)
            if type_.upper() == 'WRITE':
                return conn.commit()
            elif type_.upper() == 'READ':
                res = cur.fetchall()
                return res
            else:
                raise exceptions.WrongTypeException(
                    func_name=func_name, message=f'Unknown type: {type_}', sql=sql,
                )
        except Exception as e:
            conn.rollback()
            if type_.upper() == 'WRITE':
                raise exceptions.WriteException(
                    func_name=func_name, message=f'{e}', sql=sql, type_=type_, func_params=func_params
                )
            elif type_.upper() == 'READ':
                raise exceptions.ReadException(
                    func_name=func_name, message=f'{e}', sql=sql, type_=type_, func_params=func_params
                )
            else:
                raise exceptions.WrongTypeException(
                    func_name=func_name, message=f'Unknown type: {type_}', sql=sql,
                )

        finally:
            if self._close_conn:
                self._close()

    @staticmethod
    def _correct_input(_: t.Any):
        """
        Corrects the input to be used in the SQL query.

        :param _: The input to be corrected.
        :type _: t.Any

        :return: The corrected input.
        :rtype: t.Any
        """

        if isinstance(_, str):
            return f"'{_}'"
        else:
            return _

    def _correct_input_list(self, _: t.List[t.Any]):
        """
        Corrects the input to be used in the SQL query.

        :param _: The input to be corrected.
        :type _: t.List[t.Any]

        :return: The corrected input.
        :rtype: t.List[t.Any]
        """

        return [self._correct_input(i) for i in _]

    def _correct_input_tuple(self, _: t.Tuple[t.Any]):
        """
        Corrects the input to be used in the SQL query.

        :param _: The input to be corrected.
        :type _: t.Tuple[t.Any]

        :return: The corrected input.
        :rtype: t.Tuple[t.Any]
        """

        return tuple([self._correct_input(i) for i in _])

    def _correct_input_dict(self, _: t.Dict[str, t.Any]):
        """
        Corrects the input to be used in the SQL query.

        :param _: The input to be corrected.
        :type _: t.Dict[str, t.Any]

        :return: The corrected input.
        :rtype: t.Dict[str, t.Any]
        """

        return {k: self._correct_input(v) for k, v in _.items()}

    @staticmethod
    def _process_condition(condition: t.Union[t.List[t.Any], t.Tuple[t.Any], str]) -> str:
        sql = ''

        if type(condition) == str:
            sql += f' WHERE {condition}'

        elif type(condition) == list:
            if len(condition) < 1:
                raise ValueError(f'condition must be list with at least 1 element: {condition}')
            elif len(condition) == 1:
                sql += f' WHERE {condition[0]}'
            else:
                sql += ' WHERE ' + ' AND '.join(condition)

        elif type(condition) == tuple:
            if len(condition) < 1:
                raise ValueError(f'condition must be list with at least 1 element: {condition}')
            elif len(condition) == 1:
                sql += f' WHERE {condition[0]}'
            else:
                sql += ' WHERE ' + ' AND '.join(condition)

        else:
            raise TypeError(f'condition must be str, list or tuple: {type(condition)}')

        return sql

    def create_table(
            self, table_name: str, columns: __create_table_col_types,
            primary_key: t.Optional[str] = None, unique_keys: t.Optional[t.Union[t.List[str], t.Tuple[str], str]] = None
    ) -> None:
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" '

        if type(columns) == str:
            sql += f'({columns}'
        elif type(columns) == tuple or type(columns) == list:
            # check if columns is a list of tuples
            try:
                _ = columns[0]
                sql += "(" + ', '.join([f'{col[0]} {col[1]} ' for col in columns])
            except KeyError:
                sql += "(" + ', '.join([" ".join([f"{k} {v}" for k, v in col.items()]) for col in columns])
        elif type(columns) == dict:
            sql += "(" + f' {", ".join([f"{k} {v}" for k, v in columns.items()])}'
        else:
            raise TypeError(f'columns must be str, list or dict: {type(columns)}')

        if primary_key:
            sql += f' , PRIMARY KEY ({primary_key})'
        if unique_keys:
            if type(unique_keys) == str:
                sql += f' , UNIQUE ({unique_keys})'
            elif type(unique_keys) == tuple:
                sql += f' , UNIQUE ({", ".join([f"{k}" for k in unique_keys])})'
            elif type(unique_keys) == list:
                sql += f' , UNIQUE ({", ".join([f"{k}" for k in unique_keys])})'
            else:
                raise TypeError(f'unique_keys must be str, list or dict: {type(unique_keys)}')

        sql += ")"

        return self._execute(func_name='create_table', sql=sql, type_='WRITE', func_params=__locals__)

    def insert(
            self, table_name: str, columns: t.Union[t.List[str], t.Tuple, str, t.Dict],
            values: t.Union[t.List[str], t.Tuple, str], on_conflict: t.Optional[str] = None
    ) -> None:
        __locals__ = locals()
        __locals__.pop('self')

        sql = f'INSERT INTO "{table_name}" '

        if type(columns) == str:
            sql += f'({columns})'
        elif type(columns) == list:
            sql += f'({", ".join(columns)})'
        elif type(columns) == tuple:
            sql += f'({", ".join(columns)})'
        else:
            raise TypeError(f'columns must be str, list or tuple: {type(columns)}')

        if type(values) == str:
            sql += f' VALUES ({values})'
        elif type(values) == list:
            sql += f' VALUES ({", ".join(map(str, values))})'
        elif type(values) == tuple:
            sql += f' VALUES ({", ".join(map(str, values))})'
        else:
            raise TypeError(f'values must be str, list or tuple: {type(values)}')

        if on_conflict:
            sql += f' ON CONFLICT {on_conflict}'

        return self._execute(func_name='insert', sql=sql, type_='WRITE', func_params=__locals__)

    def insert_from_dict(self, table_name: str, data: t.Dict, on_conflict: t.Optional[str] = None):
        __locals__ = locals()
        __locals__.pop('self')

        sql = f'INSERT INTO "{table_name}" '

        sql += f'({", ".join(data.keys())})'

        sql += f''' VALUES ({", ".join(map(lambda x: f"'{x}'", data.values()))})'''

        if on_conflict:
            sql += f' ON CONFLICT {on_conflict}'

        return self._execute(func_name='insert_from_dict', sql=sql, type_='WRITE', func_params=__locals__)

    def select(
            self, table_name: str, columns: t.Union[t.List[str], t.Tuple, str], condition: t.Optional[str] = None,
            limit: t.Optional[int] = None, offset: t.Optional[int] = None, order_by: t.Optional[str] = None
    ) -> t.List[t.Tuple[t.Tuple]]:

        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'SELECT %s FROM "{table_name}"'

        if type(columns) == str:
            if columns == '*':
                sql = sql % f' {columns}'
            else:
                sql = sql % f' {columns}'
        elif type(columns) == list:
            sql = sql % f' {", ".join(columns)}'
        elif type(columns) == tuple:
            sql = sql % f' {", ".join(columns)}'
        else:
            raise TypeError(f'columns must be str, list or tuple: {type(columns)}')

        if condition:
            sql += self._process_condition(condition)
        if order_by:
            sql += f' ORDER BY {order_by}'
        if limit:
            sql += f' LIMIT {limit}'
        if offset:
            sql += f' OFFSET {offset}'

        return self._execute(func_name='select', sql=sql, type_='READ', func_params=__locals__)

    def update(
            self, table_name: str, columns: t.Union[t.List[t.Any], t.Tuple],
            values: t.Union[t.List[t.Any], t.Tuple, str], condition: t.Optional[t.Union[str, t.List, t.Tuple]] = None
    ):
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'UPDATE "{table_name}"'

        if type(columns) == str or type(values) == str:
            raise exceptions.WrongMethodException(
                'update', f'columns must be list or tuple: {type(columns)}, use `update_manual` instead'
            )

        elif type(columns) == list:
            if type(values) == list:
                if len(columns) == len(values):
                    pass
                else:
                    raise ValueError(f'columns and values must be same length: {len(columns)} != {len(values)}')
            elif type(values) == tuple:
                if len(columns) == len(values):
                    pass
                else:
                    raise ValueError(f'columns and values must be same length: {len(columns)} != {len(values)}')
            else:
                raise TypeError(f'values must be list or tuple: {type(values)}')

        elif type(columns) == tuple:
            if type(values) == list:
                if len(columns) == len(values):
                    pass
                else:
                    raise ValueError(f'columns and values must be same length: {len(columns)} != {len(values)}')
            elif type(values) == tuple:
                if len(columns) == len(values):
                    pass
                else:
                    raise ValueError(f'columns and values must be same length: {len(columns)} != {len(values)}')
            else:
                raise TypeError(f'values must be list or tuple: {type(values)}')

        else:
            raise TypeError(f'columns must be str, list or tuple: {type(columns)}')

        sql += f''' SET {", ".join(map(lambda x: f'"{x[0]}" = {self._correct_input(x[1])}', zip(columns, values)))}'''

        if condition:
            sql += self._process_condition(condition)

        return self._execute(func_name='update', sql=sql, type_='WRITE', func_params=__locals__)

    def update_via_dict(
            self, table_name: str, data: t.Dict, condition: t.Optional[t.Union[str, t.List, t.Tuple]] = None
    ) -> None:
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'UPDATE "{table_name}"'

        sql += f''' SET {", ".join([f'"{k}" = {self._correct_input(v)}' for k, v in data.items()])}'''

        if condition:
            sql += self._process_condition(condition)

        return self._execute(func_name='update_via_dict', sql=sql, type_='WRITE', func_params=__locals__)

    def update_manual(self, table_name: str, update: str, condition: str):
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'UPDATE "{table_name}" SET {update} WHERE {condition}'

        return self._execute(func_name='update_manual', sql=sql, type_='WRITE', func_params=__locals__)

    def delete(self, table_name: str, condition: t.Union[str, t.List, t.Tuple]):
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'DELETE FROM "{table_name}"'

        if condition:
            sql += self._process_condition(condition)
        else:
            raise ValueError('condition is required')

        return self._execute(func_name='delete', sql=sql, type_='WRITE', func_params=__locals__)

    def drop_table(self, table_name: str):
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = f'DROP TABLE IF EXISTS "{table_name}"'

        return self._execute(func_name='drop_table', sql=sql, type_='WRITE', func_params=__locals__)

    def create_index(
            self, table_name: str, columns: __create_index_col_types,
            unique: bool = False, index_name: t.Optional[str] = None,
            index_type: t.Optional[str] = None, index_options: t.Optional[str] = None
    ) -> None:
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        if index_type is not None and index_type.lower() not in self.__INDEX_TYPES:
            raise ValueError(f'index_type must be one of {self.__INDEX_TYPES}')

        if type(columns) == str:
            __columns = columns

        elif type(columns) == list:
            if type(columns[0]) == str:
                __columns = ', '.join(columns)
            elif type(columns[0]) == tuple or type(columns[0]) == list:
                __columns = ', '.join(map(lambda x: f'{x[0]} {x[1]}', columns))
            else:
                raise TypeError(f'Wrong type of columns: {type(columns)} | '
                                f'Available types: {self.__create_index_col_types}')

        elif type(columns) == tuple:
            if type(columns[0]) == str:
                __columns = ', '.join(columns)
            elif type(columns[0]) == tuple or type(columns[0]) == list:
                __columns = ', '.join(map(lambda x: f'{x[0]} {x[1]}', columns))
            else:
                raise TypeError(f'Wrong type of columns: {type(columns)} | '
                                f'Available types: {self.__create_index_col_types}')

        elif type(columns) == dict:
            __columns = ', '.join([f'{k} {v}' for k, v in columns.items()])

        else:
            raise TypeError(f'columns must be str, list, tuple, or dict: {type(columns)}')

        __index = 'UNIQUE INDEX' if unique else 'INDEX'
        __index_name = index_name if index_name else table_name+'_index'

        sql = f'''CREATE {__index} {__index_name} ON "{table_name}"'''

        if index_type:
            sql += f' USING {index_type}'

        if index_options is not None:
            sql += f' WITH ({index_options})'

        sql += f' ({__columns})'

        return self._execute(func_name='create_index', sql=sql, type_='WRITE', func_params=__locals__)

    def drop_index(
            self, index_name: str, concurrently: bool = None, if_exists: bool = None,
            restrict: bool = None, cascade: bool = None
    ) -> None:
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        sql = 'DROP INDEX'

        if concurrently is not None:
            sql += ' CONCURRENTLY'
        if if_exists is not None:
            sql += ' IF EXISTS'

        sql += f' "{index_name}"'

        if restrict is not None:
            sql += ' RESTRICT'
        if cascade is not None:
            sql += ' CASCADE'

        return self._execute(func_name='drop_index', sql=sql, type_='WRITE', func_params=__locals__)

    def manual_query(self, query: str, type_: str) -> t.Union[t.List, t.Tuple]:
        __locals__ = locals()
        __locals__.pop('self')
        conn = self._connect()
        cur = conn.cursor()

        return self._execute(func_name='manual_query', sql=query, type_=type_, func_params=__locals__)
