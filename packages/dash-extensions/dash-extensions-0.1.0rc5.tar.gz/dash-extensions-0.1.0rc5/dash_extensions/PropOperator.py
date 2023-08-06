# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PropOperator(Component):
    """A PropOperator component.
The PropOperator makes it possible to perform various operations on objects.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- dict (dict; optional):
    Dict operation.

- list (dict; optional):
    List operation.

    `list` is a dict with keys:

    - append (boolean | number | string | dict | list; optional) | a value equal to: 'clear'

- prop (string; optional):
    Dict operation."""
    @_explicitize_args
    def __init__(self, children=None, list=Component.UNDEFINED, prop=Component.UNDEFINED, dict=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'dict', 'list', 'prop']
        self._type = 'PropOperator'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'dict', 'list', 'prop']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(PropOperator, self).__init__(children=children, **args)
