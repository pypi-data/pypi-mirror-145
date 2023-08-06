# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ListOperator(Component):
    """A ListOperator component.
The PropOperator makes it possible to perform various operations on objects.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- apply (dict; optional):
    Apply an operation.

    `apply` is a dict with keys:

    - id (string; required)

    - operation (a value equal to: "append", "clear"; required)

    - value (boolean | number | string | dict | list; optional)

- history (list of strings; optional):
    List applied operations (just the ids).

- prop (string; optional):
    Property that this list operator binds to."""
    @_explicitize_args
    def __init__(self, children=None, apply=Component.UNDEFINED, history=Component.UNDEFINED, prop=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'apply', 'history', 'prop']
        self._type = 'ListOperator'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'apply', 'history', 'prop']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ListOperator, self).__init__(children=children, **args)
