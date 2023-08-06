# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ListStore(Component):
    """A ListStore component.
The PropOperator makes it possible to perform various operations on objects.

Keyword arguments:

- id (string; required):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- append (dict; optional):
    List operation.

    `append` is a dict with keys:

    - id (string; optional)

    - item (boolean | number | string | dict | list; optional)

- clear_data (boolean; optional):
    Set to True to remove the data contained in `data_key`.

- data (dict | list | number | string | boolean; optional):
    The stored data for the id.

- modified_timestamp (number; optional):
    The last time the storage was modified.

- storage_type (a value equal to: 'local', 'session', 'memory'; optional):
    The type of the web storage.  memory: only kept in memory, reset
    on page refresh. local: window.localStorage, data is kept after
    the browser quit. session: window.sessionStorage, data is cleared
    once the browser quit."""
    @_explicitize_args
    def __init__(self, append=Component.UNDEFINED, id=Component.REQUIRED, storage_type=Component.UNDEFINED, data=Component.UNDEFINED, clear_data=Component.UNDEFINED, modified_timestamp=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'append', 'clear_data', 'data', 'modified_timestamp', 'storage_type']
        self._type = 'ListStore'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'append', 'clear_data', 'data', 'modified_timestamp', 'storage_type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ListStore, self).__init__(**args)
