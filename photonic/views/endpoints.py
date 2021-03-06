# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
import os

from luxon import g
from luxon import GetLogger
from luxon.exceptions import AccessDenied
from luxon.utils.imports import get_class
from luxon import register_resources
from luxon import render_template
from luxon.constants import TEXT_HTML
from luxon.utils.theme import Theme
from luxon.utils.html import form

from photonic.models.endpoints import luxon_endpoint
from photonic.views.datatable import datatable

g.nav_menu.add('/System/Endpoints', href='/system/endpoints', view='role:root')

@register_resources()
class Endpoints():
    def __init__(self):
        g.router.add('GET',
                     '/system/endpoints',
                     self.list,
                     tag='role:root')

        g.router.add('GET',
                     '/system/endpoints/delete/{id}',
                     self.delete,
                     tag='role:root')

        g.router.add('GET',
                     '/system/endpoints/{id}',
                     self.view,
                     tag='role:root')

        g.router.add(('GET', 'POST',),
                     '/system/endpoints/add',
                     self.add,
                     tag='role:root')

        g.router.add(('GET', 'POST',),
                     '/system/endpoints/edit/{id}',
                     self.edit,
                     tag='role:root')

    def list(self, req, resp):
        list_html = datatable(req, 'endpoints_view',
                              '/v1/endpoints',
                              ('name', 'region'),
                              view_button=True)
        return render_template('photonic/endpoints/list.html',
                               datatable=list_html,
                               view='Endpoints')

    def delete(self, req, resp, id):
        g.client.execute('DELETE', '/v1/endpoint/%s' % id)
        resp.redirect('/system/endpoints')

    def view(self, req, resp, id):
        endpoint = g.client.execute('GET', '/v1/endpoint/%s' % id)
        html_form = form(luxon_endpoint, endpoint.json, readonly=True)
        return render_template('photonic/endpoints/view.html',
                               view='View Endpoint',
                               form=html_form,
                               id=id)

    def edit(self, req, resp, id):
        endpoint = g.client.execute('GET', '/v1/endpoint/%s' % id)
        html_form = form(luxon_endpoint, endpoint.json)
        return render_template('photonic/endpoints/edit.html',
                               view='Edit Endpoint',
                               form=html_form,
                               id=id)

    def add(self, req, resp):
        html_form = form(luxon_endpoint)
        return render_template('photonic/endpoints/add.html',
                               view='Add Endpoint',
                               form=html_form)
