#  Copyright (c) 2019 JD Williams
#
#  This file is part of Firefly, a Python SOA framework built by JD Williams. Firefly is free software; you can
#  redistribute it and/or modify it under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#
#  Firefly is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
#  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details. You should have received a copy of the GNU Lesser General Public
#  License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  You should have received a copy of the GNU General Public License along with Firefly. If not, see
#  <http://www.gnu.org/licenses/>.

from __future__ import annotations
import os
import uuid

import firefly as ff
from firefly_iaaa.application.api.generic_oauth_iam_endpoint import GenericOauthIamEndpoint
import firefly_iaaa.domain as domain


@ff.rest('/iaaa/make-client', method='POST', secured=True)
class MakeClient(GenericOauthIamEndpoint):
    _registry: ff.Registry = None

    def __call__(self, **kwargs):
        roles = []
        for role in kwargs['roles']:
            r = self._registry(domain.Role).find(lambda x: x.name == role)
            roles.append(r)
        kwargs['roles'] = roles

        tenant = domain.Tenant(
            name=kwargs['tenant_name']
        )
        kwargs['tenant'] = tenant

        kwargs['client_id'] = str(uuid.uuid4())
        kwargs['name'] = kwargs.get('name', kwargs['tenant_name'])
        kwargs = self._make_params(kwargs)

        if kwargs.get('scopes') is None or len(kwargs['scopes']) == 0:
            kwargs['scopes'] = ['iaaa.default.read']
        scopes = []
        for scope in kwargs['scopes']:
            s = self._registry(domain.Scope).find(scope)
            scopes.append(s)
        kwargs['scopes'] = scopes

        client = domain.Client.create(**kwargs)

        # Append at end to avoid appending before an error during entity creation
        self._registry(domain.Tenant).append(tenant)
        self._registry(domain.Client).append(client)
        return True

    def _make_params(self, kwargs: dict):

        self._validate_base_params(kwargs)
        grant_type = kwargs['grant_type']
        if grant_type == 'authorization_code':
            kwargs = self._add_auth_code_params(kwargs, False)
        elif grant_type == 'authorization_code_w_pkce':
            kwargs = self._add_auth_code_params(kwargs)
            kwargs['grant_type'] = 'authorization_code'
        elif grant_type == 'implicit':
            kwargs = self._add_auth_code_params(kwargs)
            kwargs['allowed_response_types'] = 'token'
        elif grant_type == 'client_credentials':
            kwargs['client_secret'] = str(uuid.uuid4())
        elif grant_type == 'password':
            name = kwargs['name']
            if name.startswith('user_tenant'):
                name = name[11:]
            kwargs['name'] = f'{name}'

        else:
            raise Exception('Invalid grant type')

        return kwargs

    def _validate_base_params(self, kwargs: dict):
        self._check_kwargs_for_fields(['scopes', 'grant_type'], kwargs)

    def _add_auth_code_params(self, kwargs: dict, uses_pkce: bool = True):
        fields = ['default_redirect_uri', 'redirect_uris']
        self._check_kwargs_for_fields(fields, kwargs)
        kwargs.update({
            'allowed_response_types': 'code',
            'uses_pkce': uses_pkce,
        })
        return kwargs

    def _get_consumer_client(self):
        client: domain.Client = self._registry(domain.Client).find(lambda x: x.client_id == os.environ['CONSUMER_CLIENT_ID'])
        tenant = client.tenant
        return client.client_id, tenant

    def _check_kwargs_for_fields(self, fields, kwargs):
        for field in fields:
            if field not in kwargs:
                raise Exception(f'Missing required field: {field}')