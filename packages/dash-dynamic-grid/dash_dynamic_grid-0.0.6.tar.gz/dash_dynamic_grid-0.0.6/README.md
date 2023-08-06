# dash-dynamic-grid

A high performance Dash data table based on the HTML5 canvas.

## How to use

First, install the python package in your Dash environment:

```pip install dash-dynamic-grid```

Next import the DynamicGrid in your python project:

```from dash_dynamic_grid import DynamicGrid```

And finally add the grid to the layout of your application:

```
app.layout = html.Div([
    DynamicGrid(
        id='my-grid',
        data=[
            {'name': 'Tomasz', 'surname': 'Rewak', 'age': 100},
            {'name': 'John', 'surname': 'Connor', 'age': 35},
            {'name': 'Ellen', 'surname': 'Ripley', 'age': -72}
        ]
    )
])
```

## Properties

##### `columns` *([] | list of (string | dict))*

The list of columns to be displayed in the grid.

If left empty, the `DynamicGrid` will automatically generate the list of columns based keys available in rows provided through the `data` property.

All *string* elements within the list of `coulmns` will be converted into column definitions of same `id` and `name` as the provided value.

Each column definition can consist of:
- `format` *(js expression; default ``'`${value}`'``)*: A JavaScript expression that transforms the value of a cell into a string that will be displayed within the grid. Within that expression one has access to the following values: 
  - `value` *(any)*: Value obtained from the row definition by using the `id` of the current column.
  - `row` *(dict)*: The row from which the cell comes from.
  - `rowIndex` *(number)*: 0-based index of the current row.
  - `column` *(string)*: Id of the column.
  - `data` *(list of dicts)*: Full data set used by the grid.
- `header` *(string; default `id`)*: The header text to be displayed at the top of the column.
- `id` *(string; required)*: A unique identifier of a column. It is used both to retrieve the value of a cell from the row definition, as well as to uniquely identify that row during selection.
- `style` *(js expression|js expression[]; default `'{}'`)*: A JavaScript expression that produces the style of a cell based on its value. Within that expression one has access to the following values: 
  - `value` *(any)*: Value obtained from the row definition by using the `id` of the current column.
  - `row` *(dict)*: The row from which the cell comes from.
  - `rowIndex` *(number)*: 0-based index of the row within the `data`.
  - `column` *(string)*: Id of the column.
  - `data` *(list of dicts)*: Full data set used by the grid.

  The produced style can have following fields:
  - `align` *(`'left'`|`'right'`|`'center'`|None; default None)*: Text alignemnt within the column.
  - `background` *(string; default `'white'`)*: Background color of the cell.
  - `foreground` *(string; default `'black'`)*: Foreground color of the cell.
  - `dataBar` *(object: {min: number, value: number, max: number})*: Data bar indicator.

  Instead of a single style expression, an array of expressions can be provided. In that case expresions will be evaluated in the provided order and the last value of each field will be used to style the cell.
- `tooltip` *(js expression)*: A JavaScript expression that produces a string tooltip for a cell. Within that expression one has access to the following values: 
  - `value` *(any)*: Value obtained from the row definition by using the `id` of the current column.
  - `row` *(dict)*: The row from which the cell comes from.
  - `rowIndex` *(number)*: 0-based index of the row within the `data`.
  - `column` *(string)*: Id of the column.
  - `data` *(list of dicts)*: Full data set used by the grid.
- `width` *(`'fit'`|number; default `'fit'`)*: Width of the column. If set to `'fit'`, the width of the column will be adjusted automatically to fit its content. If set to *number*, the column will be that amount of pixels wide.

Example values:
```
columns=[
    'column_1',
    { 'id': 'column_2', 'header': '_c_' },
    {
        'id': 'column_3',
        'align': 'left',
        'width': '100',
        'format': 'value.toFixed(2)',
        'style': 'rowIndex % 2 == 0 ? { background: "lightgray" } : { }',
        'tooltip': '`speed: ${value} km/h`'
    },
    {
        'id': 'column_4',
        'format': 'value > 2 ? "big" : "small"',
        'style': '{ background: interpolateColors(-1, value, 4, colorScales.redBlueGreen) }',
        'tooltip': '`column_1: ${row["column_1"]} \n column_2: ${row["column_2"]}`'
    }
]
```

---

##### `data` *(list of dicts; defaul `[]`)*

The list of rows to be displayed in the object.

If no `columns` are specified in the `DynamicGrid` component, the `DynamicGrid` will automatically generate the list of columns based keys available in provided rows.

Example values:
```
data=[]
```
```
data=[
    {'name': 'Tomasz', 'surname': 'Rewak', 'age': 100},
    {'name': 'John', 'surname': 'Connor', 'age': 35},
    {'name': 'Ellen', 'surname': 'Ripley', 'age': -72}
]
```
```
data=pandas_data_frame.to_dict('records')
```

---

##### `id` *(string)* 

The standard Dash component identification key. Can be used to set other properties of this component through callbacks.
