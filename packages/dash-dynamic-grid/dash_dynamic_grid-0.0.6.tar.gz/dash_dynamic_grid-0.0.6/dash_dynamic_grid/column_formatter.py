from typing import Union, List, Dict


__column = Union[str, Dict]
__resolved_column = Dict
__columns = List[__column]
__ids = List[str]


def __resolve_column_structure(column: __column) -> __resolved_column:
    if isinstance(column, str):
        return {'id': column}

    return column


def __is_included(column: __column, include_columns: __ids, exclude_columns: __ids) -> bool:
    id = column['id'] if isinstance(column, dict) else column

    if include_columns and id in include_columns:
        return True

    if exclude_columns and id in exclude_columns:
        return False

    return not include_columns


def __apply_to_all_columns(columns: __columns, transformation, include_columns: __ids, exclude_columns: __ids) -> __columns:
    return [
        transformation(column) if __is_included(column, include_columns, exclude_columns) else column
        for column in columns
    ]


def __set_header(column: __column, header: str) -> __resolved_column:
    resolved_column = __resolve_column_structure(column)

    return {**resolved_column, **{'header': header}}


def set_header(columns: __columns, header: str, include_columns: __ids = None, exclude_columns: __ids = None) -> __columns:
    return __apply_to_all_columns(
        columns,
        lambda column: __set_header(column, header),
        include_columns,
        exclude_columns)


def __set_numeric_format(column: __column, precision: int, empty_value: str) -> __resolved_column:
    resolved_column = __resolve_column_structure(column)

    return {**resolved_column, **{'format': f'value == null ? "{empty_value}" : value.toFixed({precision})' }}


def set_numeric_format(columns: __columns, precision: int = 2, empty_value: str = '', include_columns: __ids = None, exclude_columns: __ids = None) -> __columns:
    return __apply_to_all_columns(
        columns,
        lambda column: __set_numeric_format(column, precision, empty_value),
        include_columns,
        exclude_columns)