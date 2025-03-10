# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 National Institute of Informatics.
#
# WEKO-Items-Autofill is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module of weko-items-autofill."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, jsonify, render_template, request
from flask_babelex import gettext as _
from flask_login import login_required
from weko_accounts.utils import login_required_customize
from weko_admin.utils import get_current_api_certification

from .utils import get_cinii_record_data, get_crossref_record_data, \
    get_title_pubdate_path, get_wekoid_record_data, get_workflow_journal

blueprint = Blueprint(
    "weko_items_autofill",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/autofill",
)

blueprint_api = Blueprint(
    "weko_items_autofill",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/autofill",
)


@blueprint.route("/")
def index():
    """Render a basic view."""
    return render_template(
        "weko_items_autofill/index.html", module_name=_("WEKO-Items-Autofill")
    )


@blueprint_api.route('/select_options', methods=['GET'])
@login_required_customize
def get_selection_option():
    """Get metadata  select options.

    :return: json: Metadata select options
    """
    options = [{'value': 'Default', 'text': _('Select the ID')}]
    options.extend(current_app.config['WEKO_ITEMS_AUTOFILL_SELECT_OPTION'])
    result = {
        'options': options
    }
    return jsonify(result)


@blueprint_api.route('/get_title_pubdate_id/<int:item_type_id>',
                     methods=['GET'])
@login_required_customize
def get_title_pubdate_id(item_type_id=0):
    """Get title and pubdate id.

    :param item_type_id:
    :return: result json
    """
    result = get_title_pubdate_path(item_type_id)
    return jsonify(result)


@blueprint_api.route('/get_auto_fill_record_data', methods=['POST'])
@login_required_customize
def get_auto_fill_record_data():
    """Get auto fill record data.

    :return: record model as json
    """
    result = {
        'result': '',
        'items': '',
        'error': ''
    }
    if request.headers['Content-Type'] != 'application/json':
        result['error'] = _('Header Error')
        return jsonify(result)

    data = request.get_json()
    api_type = data.get('api_type', '')
    search_data = data.get('search_data', '')
    item_type_id = data.get('item_type_id', '')

    try:
        if api_type == 'CrossRef':
            pid_response = get_current_api_certification('crf')
            pid = pid_response['cert_data']
            api_response = get_crossref_record_data(
                pid, search_data, item_type_id)
            result['result'] = api_response
        elif api_type == 'CiNii':
            api_response = get_cinii_record_data(
                search_data, item_type_id)
            result['result'] = api_response
        elif api_type == 'WEKOID':
            result['result'] = get_wekoid_record_data(
                search_data, item_type_id)
        else:
            result['error'] = api_type + ' is NOT support autofill feature.'
    except Exception as e:
        result['error'] = str(e)

    return jsonify(result)


@blueprint_api.route('/get_auto_fill_journal/<string:activity_id>',
                     methods=['GET'])
@login_required_customize
def get_item_auto_fill_journal(activity_id):
    """Get workflow journal data.

    :param activity_id: The identify of Activity.
    :return: Workflow journal data.
    """
    result = dict()
    result['result'] = get_workflow_journal(activity_id)

    return jsonify(result)
