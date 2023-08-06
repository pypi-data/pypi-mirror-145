import re
import sqlite3
from collections import namedtuple

from litetable import utils


class LiteTable:
    DEFAULT_CONN = None

    def __init__(self, data=None, columns=None, table_name=None, conn=None):
        """

        Parameters
        ----------
        data : list[dict]
        columns : list[str], optional
        table_name : str, optional
            Use an existing table.
        conn : sqlite3.Connection, optional
        """
        if table_name is None and data is None and columns is None:
            raise ValueError('Please either provide data or column names')

        if conn is None:
            # Build the default connection object
            if self.DEFAULT_CONN is None:
                conn = sqlite3.connect(':memory:')
                conn.row_factory = namedtuple_factory
                self.__class__.DEFAULT_CONN = conn

            conn = self.DEFAULT_CONN
        self.conn = conn

        if table_name is not None:
            self.table_name = table_name
            return

        self.table_name = utils.make_random_table_name()

        data = utils.normalize_data(data)
        # Generate alphabetical column names if column names are not provided
        if columns is None:
            obj = data[0]
            columns = utils.extract_column_names(obj)
            if columns is None:
                columns = [f'c{i + 1}' for i in range(len(obj))]

        columns_sql = ', '.join([utils.escape_literal(col) for col in columns])
        sql = f'CREATE TABLE {self.table_identifier} ({columns_sql})'

        self.conn.cursor().execute(sql)
        self.append_many(data)

    def __call__(self, query):
        q = query.strip().lower()
        if not q.startswith('select') and not q.startswith('with'):
            raise ValueError('Only statements starting with SELECT or WITH '
                             'are allowed')

        query = self._replace_placeholders(query)
        new_table_name = utils.make_random_table_name()
        sql = f'CREATE TABLE {new_table_name} AS {query}'
        self.conn.cursor().execute(sql)
        return LiteTable(table_name=new_table_name)

    def __del__(self):
        sql = f'DROP TABLE {self.table_name}'
        self.conn.cursor().execute(sql)

    def __getattr__(self, item):
        if item in self.columns:
            return self.col(item)

        raise AttributeError(f"'LiteTable' object has no attribute or column "
                             f"'{item}'")

    def __getitem__(self, item):
        """Numpy style 2d array access to LiteTable data

        Parameters
        ----------
        item

        """
        where = item
        select = None
        group_by = None

        if isinstance(item, tuple):
            where = item[0]
            if len(item) >= 2:
                select = item[1]
            if len(item) >= 3:
                group_by = item[2]
            if len(item) >= 4:
                raise IndexError('Too many index values supplied')

        # Resolve WHERE
        single_row = False
        where_sql = ''
        if isinstance(where, int):
            single_row = True
            if where < 0:
                where = len(self) + where

            rowid = self._resolve_rowid(where)
            where_sql = f'WHERE rowid = {rowid}'
        elif isinstance(where, str):
            where_sql = f'WHERE {where}'
        elif isinstance(where, slice):
            if where.step is not None:
                raise ValueError('Step parameter in slice is not currently '
                                 'supported')

            start = where.start
            stop = where.stop

            # Translate negative indices to positive
            if start and start < 0:
                start = len(self) + start

            if stop:
                if stop < 0:
                    stop = len(self) + stop

                if stop == 0:
                    stop = None

            where_conditions = []
            if start is not None and start != 0:
                start = self._resolve_rowid(start)
                where_conditions.append(f'ROWID >= {start}')
            if stop is not None:
                stop_inclusive = self._resolve_rowid(stop - 1)
                where_conditions.append(f'ROWID <= {stop_inclusive}')

            if where_conditions:
                where_condition = ' AND '.join(where_conditions)
                where_sql = f'WHERE {where_condition}'

        else:
            raise ValueError(f"Unsupported row selector: '{where}' "
                             f"({type(where).__name__})")

        # Resolve SELECT
        single_col = False
        if select is None:
            select_sql = 'SELECT *'
        elif isinstance(select, int):
            single_col = True
            select_sql = f'SELECT {self._col_identifiers[select]}'
        elif isinstance(select, str):
            select_sql = f'SELECT {select}'
        elif isinstance(select, slice):
            start = select.start
            stop = select.stop

            # Change strings to col indices
            if isinstance(start, str):
                start = self.index(start)
            if isinstance(stop, str):
                # Note that with strings, we include the last column
                stop = self.index(stop) + 1

            s = slice(start, stop, select.step)
            cols_str = ', '.join(self._col_identifiers[s])
            select_sql = f'SELECT {cols_str}'
        else:
            raise ValueError(f"Unsupported column selector: '{select}' "
                             f"({type(select).__name__})")

        # Resolve GROUP BY
        if group_by is None:
            group_by_sql = ''
        elif isinstance(group_by, str):
            group_by_sql = f'GROUP BY {group_by}'

        # Execute
        sql = f'{select_sql} FROM {self.table_name} {where_sql} {group_by_sql}'
        if single_row:
            cursor = self.conn.cursor().execute(sql)
            res = next(cursor)
            if single_col:
                res = res[0]
        elif single_col:
            cursor = self.conn.cursor().execute(sql)
            res = [row[0] for row in cursor]
        else:
            res = self(sql)

        return res

    def __iter__(self):
        sql = f'SELECT * FROM {self.table_name}'
        return self.conn.cursor().execute(sql)

    def __repr__(self):
        sql = f'SELECT * FROM {self.table_name} LIMIT 5'
        c = self.conn.cursor().execute(sql)
        column_names = [desc[0] for desc in c.description]
        # TODO: improve formatting
        s = '   ' + ', '.join(column_names) + '\n'
        for i, row in enumerate(c.fetchall()):
            row = [str(v) for v in row]
            s += f"{i}: {', '.join(row)}\n"
        return s

    def __len__(self):
        sql = f'SELECT COUNT(*) FROM {self.table_name}'
        return self.conn.cursor().execute(sql).fetchone()[0]

    def append(self, row):
        """Append

        Parameters
        ----------
        row : dict or list or tuple

        Returns
        -------
        None
        """
        return self.append_many([row])

    def append_many(self, rows):
        """Append many rows at one go

        Parameters
        ----------
        rows : list[dict] or list[list] or list[tuple]

        Returns
        -------
        None
        """
        if not rows:
            return

        colnames = []
        first_row = rows[0]
        if isinstance(first_row, dict):
            # Build values list of lists
            prepared_values = [list(dict_.values()) for dict_ in rows]
            # Extract column names
            colnames = list(first_row.keys())
        elif utils.is_namedtuple(first_row):
            prepared_values = rows
            fields = list(first_row._fields)
            # We need to use namedtuple colnames to match colnames to
            cols_as_fields = utils.format_namedtuple_names(self.columns)
            colnames = []
            for field in fields:
                try:
                    i = cols_as_fields.index(field)
                except ValueError:
                    raise ValueError(f"Column '{field}' not found")

                colnames.append(self.columns[i])
        elif isinstance(first_row, (list, tuple)):
            prepared_values = rows
        else:
            raise ValueError(f'Values of type {type(first_row).__name__} '
                             f'are not currently supported')

        value_literals = ', '.join('?' * len(first_row))
        escaped_colnames = [utils.escape_identifier(col) for col in colnames]
        column_identifiers = ', '.join(escaped_colnames)
        if column_identifiers:
            column_identifiers = f'({column_identifiers})'
        sql = f'INSERT INTO {self.table_identifier} {column_identifiers} ' \
              f'VALUES ({value_literals})'
        self.conn.cursor().executemany(sql, prepared_values)

    def col(self, col_name):
        return self[:, self.index(col_name)]

    @property
    def columns(self):
        sql = f'PRAGMA table_info({self.table_name});'
        cursor = self.conn.cursor().execute(sql)
        return [c[1] for c in cursor]

    def index(self, col_name):
        try:
            return self.columns.index(col_name)
        except ValueError:
            raise ValueError(f"Column '{col_name}' is not in the table")

    def execute(self, query):
        query = self._replace_placeholders(query)
        return self.conn.cursor().execute(query)

    @property
    def table_identifier(self):
        return utils.escape_identifier(self.table_name)

    @property
    def _col_identifiers(self):
        return [utils.escape_identifier(col) for col in self.columns]

    def _replace_placeholders(self, query):
        # Replace :this
        return re.sub(r':this([\s\.]?)', f'{self.table_identifier}\\1', query)

    def _resolve_rowid(self, index):
        rowid = self.conn.cursor().execute(
            f'SELECT rowid FROM {self.table_name} LIMIT 1 OFFSET {index}'
        )
        rowid = list(rowid)
        if not rowid:
            raise IndexError(f'Row index {index} out of range')

        return rowid[0][0]


def namedtuple_factory(cursor, row):
    """Returns sqlite rows as named tuples."""
    fields = [col[0] for col in cursor.description]
    Row = namedtuple("Row", utils.format_namedtuple_names(fields))
    return Row(*row)
