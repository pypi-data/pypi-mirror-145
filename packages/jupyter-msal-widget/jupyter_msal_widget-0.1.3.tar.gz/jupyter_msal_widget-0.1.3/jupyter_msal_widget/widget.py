#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Felipe Oucharski.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""
from ipywidgets import DOMWidget, VBox, widget_serialization
from traitlets import Unicode, Bool, Dict, Instance, default
from ._frontend import module_name, module_version

class MsalWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('MsalWidgetModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('MsalWidgetView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    client_id = Unicode('').tag(sync=True)
    authority_url = Unicode('').tag(sync=True)

    signed_in = Bool(False).tag(sync=True)
    account = Dict({}).tag(sync=True)
    
    display_logout = Bool(False).tag(sync=True)
    button_main_color = Unicode('0, 117, 190').tag(sync=True)
    button_style = Dict({"float":"right"}).tag(sync=True)
    container_style = Dict({}).tag(sync=True)
    content = Instance(VBox).tag(sync=True, **widget_serialization)




