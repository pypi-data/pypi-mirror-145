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
from datetime import datetime, timedelta
from typing import List, Union

import firefly as ff
from oauthlib.oauth2 import RequestValidator
from oauthlib.common import Request

from firefly_iaaa import domain


class OauthRequestValidators(RequestValidator):
    _registry: ff.Registry = None
    _valid_token_type_hints: List[str] = ['refresh_token', 'access_token']
    _secret_key: str = None
    _kernel: ff.Kernel = None
    _decode_token: domain.DecodeToken = None

    def authenticate_client(self, request: Request, *args, **kwargs):
        """Authenticate client through means outside the OAuth 2 spec.

        Means of authentication is negotiated beforehand and may for example
        be `HTTP Basic Authentication Scheme`_ which utilizes the Authorization
        header.

        Headers may be accesses through request.headers and parameters found in
        both body and query can be obtained by direct attribute access, i.e.
        request.client_id for client_id in the URL query.
		
        The authentication process is required to contain the identification of
        the client (i.e. search the database based on the client_id). In case the
        client doesn't exist based on the received client_id, this method has to
        return False and the HTTP response created by the library will contain
        'invalid_client' message. 

        After the client identification succeeds, this method needs to set the
        client on the request, i.e. request.client = client. A client object's
        class must contain the 'client_id' attribute and the 'client_id' must have
        a value.

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
            - Resource Owner Password Credentials Grant (may be disabled)
            - Client Credentials Grant
            - Refresh Token Grant

        .. _`HTTP Basic Authentication Scheme`: https://tools.ietf.org/html/rfc1945#section-11.1
        """

        return self._http_headers_authentication(request)

    def authenticate_client_id(self, client_id: str, request: Request, *args, **kwargs):
        """Ensure client_id belong to a non-confidential client.

        A non-confidential client is one that is not required to authenticate
        through other means, such as using HTTP Basic.

        Note, while not strictly necessary it can often be very convenient
        to set request.client to the client object associated with the
        given client_id.

        :param client_id: Unicode client identifier.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
        """
        if self.validate_client_id(client_id, request):
            if not request.client.is_confidential() or request.grant_type == 'refresh_token':
                return True
        return False

    def client_authentication_required(self, request: Request, *args, **kwargs):
        """Determine if client authentication is required for current request.

        According to the rfc6749, client authentication is required in the following cases:
            - Resource Owner Password Credentials Grant, when Client type is Confidential or when
              Client was issued client credentials or whenever Client provided client
              authentication, see `Section 4.3.2`_.
            - Authorization Code Grant, when Client type is Confidential or when Client was issued
              client credentials or whenever Client provided client authentication,
              see `Section 4.1.3`_.
            - Refresh Token Grant, when Client type is Confidential or when Client was issued
              client credentials or whenever Client provided client authentication, see
              `Section 6`_

        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
            - Resource Owner Password Credentials Grant
            - Refresh Token Grant

        .. _`Section 4.3.2`: https://tools.ietf.org/html/rfc6749#section-4.3.2
        .. _`Section 4.1.3`: https://tools.ietf.org/html/rfc6749#section-4.1.3
        .. _`Section 6`: https://tools.ietf.org/html/rfc6749#section-6
        """
        #Always authenticate when headers are present
        if (request.body.get('username') and request.body.get('password')) or request.body.get('client_secret'):
            return True
        client: domain.Client = self._get_client(request.client_id)
        if not client:
            return False
        return client.is_confidential() and request.grant_type != 'refresh_token'

    def confirm_redirect_uri(self, client_id: str, code: str, redirect_uri: str, client: domain.Client, request: Request, *args, **kwargs):
        """Ensure that the authorization process represented by this authorization
        code began with this 'redirect_uri'.

        If the client specifies a redirect_uri when obtaining code then that
        redirect URI must be bound to the code and verified equal in this
        method, according to RFC 6749 section 4.1.3.  Do not compare against
        the client's allowed redirect URIs, but against the URI used when the
        code was saved.

        :param client_id: Unicode client identifier.
        :param code: Unicode authorization_code.
        :param redirect_uri: Unicode absolute URI.
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant (during token request)
        """
        auth_code: domain.AuthorizationCode = self._get_authorization_code(code)
        if not auth_code:
            return False
        return auth_code.client.client_id == client.client_id and auth_code.validate_redirect_uri(redirect_uri)

    def get_code_challenge(self, code: str, request: Request):
        """Is called for every "token" requests.

        When the server issues the authorization code in the authorization
        response, it MUST associate the ``code_challenge`` and
        ``code_challenge_method`` values with the authorization code so it can
        be verified later.

        Typically, the ``code_challenge`` and ``code_challenge_method`` values
        are stored in encrypted form in the ``code`` itself but could
        alternatively be stored on the server associated with the code.  The
        server MUST NOT include the ``code_challenge`` value in client requests
        in a form that other entities can extract.

        Return the ``code_challenge`` associated to the code.
        If ``None`` is returned, code is considered to not be associated to any
        challenges.

        :param code: Authorization code.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: code_challenge string

        Method is used by:
            - Authorization Code Grant - when PKCE is active

        """

        auth_code: domain.AuthorizationCode = self._get_authorization_code(code)

        if not auth_code:
            return None
        return auth_code.challenge

    def get_code_challenge_method(self, code: str, request: Request):
        """Is called during the "token" request processing, when a
        ``code_verifier`` and a ``code_challenge`` has been provided.

        See ``.get_code_challenge``.

        Must return ``plain`` or ``S256``. You can return a custom value if you have
        implemented your own ``AuthorizationCodeGrant`` class.

        :param code: Authorization code.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: code_challenge_method string

        Method is used by:
            - Authorization Code Grant - when PKCE is active

        """

        auth_code: domain.AuthorizationCode = self._get_authorization_code(code)

        if not auth_code:
            return None
        return auth_code.challenge_method

    def get_default_redirect_uri(self, client_id: str, request: Request, *args, **kwargs):
        """Get the default redirect URI for the client.

        :param client_id: Unicode client identifier.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: The default redirect URI for the client

        Method is used by:
            - Authorization Code Grant
            - Implicit Grant
        """
        return request.client.default_redirect_uri

    def get_default_scopes(self, client_id: str, request: Request, *args, **kwargs):
        """Get the default scopes for the client.

        :param client_id: Unicode client identifier.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: List of default scopes

        Method is used by all core grant types:
            - Authorization Code Grant
            - Implicit Grant
            - Resource Owner Password Credentials Grant
            - Client Credentials grant
        """
        return getattr(request, 'login_scopes', request.client.get_scopes())

    def get_original_scopes(self, refresh_token: str, request: Request, *args, **kwargs):
        """Get the list of scopes associated with the refresh token.

        :param refresh_token: Unicode refresh token.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: List of scopes.

        Method is used by:
            - Refresh token grant
        """
        bearer_token: domain.BearerToken
        bearer_token, _ = self._get_bearer_token(refresh_token, 'refresh_token')
        if not bearer_token:
            return None
        return bearer_token.get_scopes()

    def introspect_token(self, token: str, token_type_hint: str, request: Request, *args, **kwargs):
        """Introspect an access or refresh token.

        Called once the introspect request is validated. This method should
        verify the *token* and either return a dictionary with the list of
        claims associated, or `None` in case the token is unknown.

        Below the list of registered claims you should be interested in:
        - scope : space-separated list of scopes
        - client_id : client identifier
        - username : human-readable identifier for the resource owner
        - token_type : type of the token
        - exp : integer timestamp indicating when this token will expire
        - iat : integer timestamp indicating when this token was issued
        - nbf : integer timestamp indicating when it can be "not-before" used
        - sub : subject of the token - identifier of the resource owner
        - aud : list of string identifiers representing the intended audience
        - iss : string representing issuer of this token
        - jti : string identifier for the token

        Note that most of them are coming directly from JWT RFC. More details
        can be found in `Introspect Claims`_ or `_JWT Claims`_.

        The implementation can use *token_type_hint* to improve lookup
        efficency, but must fallback to other types to be compliant with RFC.

        The dict of claims is added to request.token after this method.

        :param token: The token string.
        :param token_type_hint: access_token or refresh_token.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request

        Method is used by:
            - Introspect Endpoint (all grants are compatible)

        .. _`Introspect Claims`: https://tools.ietf.org/html/rfc7662#section-2.2
        .. _`JWT Claims`: https://tools.ietf.org/html/rfc7519#section-4
        """

        bearer_token: domain.BearerToken
        bearer_token, token_type = self._get_bearer_token(token, token_type_hint)
        if bearer_token is None:
            request.token = None
            return
        resp = self._generate_introspection_response(bearer_token, token, token_type, request)
        request.token = resp
        return resp

    def invalidate_authorization_code(self, client_id: str, code: dict, request: Request, *args, **kwargs):
        """Invalidate an authorization code after use.

        :param client_id: Unicode client identifier.
        :param code: The authorization code grant (request.code).
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request

        Method is used by:
            - Authorization Code Grant
        """

        auth_code: domain.AuthorizationCode = self._get_authorization_code(code)

        if not auth_code:
            return
        auth_code.invalidate()

    def is_pkce_required(self, client_id: str, request: Request):
        """Determine if current request requires PKCE. Default, False.
        This is called for both "authorization" and "token" requests.

        Override this method by ``return True`` to enable PKCE for everyone.
        You might want to enable it only for public clients.
        Note that PKCE can also be used in addition of a client authentication.

        OAuth 2.0 public clients utilizing the Authorization Code Grant are
        susceptible to the authorization code interception attack.  This
        specification describes the attack as well as a technique to mitigate
        against the threat through the use of Proof Key for Code Exchange
        (PKCE, pronounced "pixy"). See `RFC7636`_.

        :param client_id: Client identifier.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant

        .. _`RFC7636`: https://tools.ietf.org/html/rfc7636
        """

        return request.client.requires_pkce()

    def is_within_original_scope(self, request_scopes: List[str], refresh_token: str, request: Request, *args, **kwargs):
        """Check if requested scopes are within a scope of the refresh token.

        When access tokens are refreshed the scope of the new token
        needs to be within the scope of the original token. This is
        ensured by checking that all requested scopes strings are on
        the list returned by the get_original_scopes. If this check
        fails, is_within_original_scope is called. The method can be
        used in situations where returning all valid scopes from the
        get_original_scopes is not practical.

        :param request_scopes: A list of scopes that were requested by client.
        :param refresh_token: Unicode refresh_token.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Refresh token grant
        """

        bearer_token: domain.BearerToken
        bearer_token, _ = self._get_bearer_token(refresh_token, 'refresh_token')

        if not bearer_token:
            return False
        return bearer_token.validate_scopes(request_scopes)

    def rotate_refresh_token(self, request):
        return True

    def revoke_token(self, token: str, token_type_hint: str, request: Request, *args, **kwargs):
        """Revoke an access or refresh token.

        :param token: The token string.
        :param token_type_hint: access_token or refresh_token.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request

        Method is used by:
            - Revocation Endpoint
        """
        bearer_token: domain.BearerToken
        bearer_token, token_type = self._get_bearer_token(token, token_type_hint)

        if not bearer_token:
            return
        if token_type == 'refresh_token':
            bearer_token.invalidate()
        else:
            bearer_token.invalidate_access_token()

    def save_authorization_code(self, client_id: str, code: dict, request: Request, *args, **kwargs):
        """Persist the authorization_code.

        The code should at minimum be stored with:
            - the client_id (``client_id``)
            - the redirect URI used (``request.redirect_uri``)
            - a resource owner / user (``request.user``)
            - the authorized scopes (``request.scopes``)

        To support PKCE, you MUST associate the code with:
            - Code Challenge (``request.code_challenge``) and
            - Code Challenge Method (``request.code_challenge_method``)

        To support OIDC, you MUST associate the code with:
            - nonce, if present (``code["nonce"]``)

        The ``code`` argument is actually a dictionary, containing at least a
        ``code`` key with the actual authorization code:

            ``{'code': 'sdf345jsdf0934f'}``

        It may also have a ``claims`` parameter which, when present, will be a dict
        deserialized from JSON as described at
        http://openid.net/specs/openid-connect-core-1_0.html#ClaimsParameter
        This value should be saved in this method and used again in ``.validate_code``.

        :param client_id: Unicode client identifier.
        :param code: A dict of the authorization code grant and, optionally, state.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request

        Method is used by:
            - Authorization Code Grant
        """
        auth_code = self._generate_authorization_code(code, request, kwargs.get('claims'))
        self._registry(domain.AuthorizationCode).append(auth_code)

    def save_bearer_token(self, token: dict, request: Request, *args, **kwargs):
        """Persist the Bearer token.

        The Bearer token should at minimum be associated with:
            - a client and it's client_id, if available
            - a resource owner / user (request.user)
            - authorized scopes (request.scopes)
            - an expiration time
            - a refresh token, if issued
            - a claims document, if present in request.claims

        The Bearer token dict may hold a number of items::

            {
                'token_type': 'Bearer',
                'access_token': 'askfjh234as9sd8',
                'expires_in': 3600,
                'scope': 'string of space separated authorized scopes',
                'refresh_token': '23sdf876234',  # if issued
                'state': 'given_by_client',  # if supplied by client (implicit ONLY)
            }

        Note that while "scope" is a string-separated list of authorized scopes,
        the original list is still available in request.scopes.

        The token dict is passed as a reference so any changes made to the dictionary
        will go back to the user.  If additional information must return to the client
        user, and it is only possible to get this information after writing the token
        to storage, it should be added to the token dictionary.  If the token
        dictionary must be modified but the changes should not go back to the user,
        a copy of the dictionary must be made before making the changes.

        Also note that if an Authorization Code grant request included a valid claims
        parameter (for OpenID Connect) then the request.claims property will contain
        the claims dict, which should be saved for later use when generating the
        id_token and/or UserInfo response content.

        :param token: A Bearer token dict.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: The default redirect URI for the client

        Method is used by all core grant types issuing Bearer tokens:
            - Authorization Code Grant
            - Implicit Grant
            - Resource Owner Password Credentials Grant (might not associate a client)
            - Client Credentials grant
        """
        bearer_token = self._generate_bearer_token(token, request)
        self._registry(domain.BearerToken).append(bearer_token)

        try:
            request.old_token.invalidate()
        except AttributeError:
            pass
        return request.client.default_redirect_uri

    def validate_bearer_token(self, token: str, scopes: List[str], request: Request):
        """Ensure the Bearer token is valid and authorized access to scopes.

        :param token: A string of random characters.
        :param scopes: A list of scopes associated with the protected resource.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request

        A key to OAuth 2 security and restricting impact of leaked tokens is
        the short expiration time of tokens, *always ensure the token has not
        expired!*.

        Two different approaches to scope validation:

            1) all(scopes). The token must be authorized access to all scopes
                            associated with the resource. For example, the
                            token has access to ``read-only`` and ``images``,
                            thus the client can view images but not upload new.
                            Allows for fine grained access control through
                            combining various scopes.

            2) any(scopes). The token must be authorized access to one of the
                            scopes associated with the resource. For example,
                            token has access to ``read-only-images``.
                            Allows for fine grained, although arguably less
                            convenient, access control.

        A powerful way to use scopes would mimic UNIX ACLs and see a scope
        as a group with certain privileges. For a restful API these might
        map to HTTP verbs instead of read, write and execute.

        Note, the request.user attribute can be set to the resource owner
        associated with this token. Similarly the request.client and
        request.scopes attribute can be set to associated client object
        and authorized scopes. If you then use a decorator such as the
        one provided for django these attributes will be made available
        in all protected views as keyword arguments.

        :param token: Unicode Bearer token
        :param scopes: List of scopes (defined by you)
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is indirectly used by all core Bearer token issuing grant types:
            - Authorization Code Grant
            - Implicit Grant
            - Resource Owner Password Credentials Grant
            - Client Credentials Grant
        """
        bearer_token: domain.BearerToken
        bearer_token, token_type = self._get_bearer_token(token)

        if not bearer_token or token_type != 'access_token':
            return False
        decoded_token = self._decode_token(token, bearer_token.client.client_id)
        try:
            for scope in scopes:
                if scope not in decoded_token['scope'].split(' '):
                    return False
        except TypeError:
            scopes = decoded_token['scope'].split(' ')
        if bearer_token.validate(scopes):
            request.user = bearer_token.user
            request.client = bearer_token.client
            request.scopes = bearer_token.get_scopes()
            return True
        return False

    def validate_client_id(self, client_id: str, request: Request, *args, **kwargs):
        """Ensure client_id belong to a valid and active client.

        Note, while not strictly necessary it can often be very convenient
        to set request.client to the client object associated with the
        given client_id.

        :param client_id: Unicode client identifier.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
            - Implicit Grant
        """
        client: domain.Client = request.client or self._get_client(client_id)

        if not client:
            return False
        if client.validate():
            request.client = client
            return True
        return False

    def validate_code(self, client_id: str, code: str, client: domain.Client, request: Request, *args, **kwargs):
        """Verify that the authorization_code is valid and assigned to the given
        client.

        Before returning true, set the following based on the information stored
        with the code in 'save_authorization_code':

            - request.user
            - request.scopes
            - request.claims (if given)
        OBS! The request.user attribute should be set to the resource owner
        associated with this authorization code. Similarly request.scopes
        must also be set.

        The request.claims property, if it was given, should assigned a dict.

        If PKCE is enabled (see 'is_pkce_required' and 'save_authorization_code')
        you MUST set the following based on the information stored:
            - request.code_challenge
            - request.code_challenge_method

        :param client_id: Unicode client identifier.
        :param code: Unicode authorization code.
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
        """

        auth_code: domain.AuthorizationCode = self._get_authorization_code(code)

        if not auth_code:
            return False
        if auth_code.validate(client.client_id):
            request.user = auth_code.user
            request.scopes = auth_code.get_scopes()
            if auth_code.claims:
                request.claims = auth_code.claims 
            if client.requires_pkce():
                if auth_code.challenge:
                    request.code_challenge = auth_code.challenge
                if auth_code.challenge_method:
                    request.code_challenge_method = auth_code.challenge_method
            return True
        return False

    def validate_grant_type(self, client_id: str, grant_type: str, client: domain.Client, request: Request, *args, **kwargs):
        """Ensure client is authorized to use the grant_type requested.

        :param client_id: Unicode client identifier.
        :param grant_type: Unicode grant type, i.e. authorization_code, password.
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
            - Resource Owner Password Credentials Grant
            - Client Credentials Grant
            - Refresh Token Grant
        """
        return client.validate_grant_type(grant_type)

    def validate_redirect_uri(self, client_id: str, redirect_uri: str, request: Request, *args, **kwargs):
        """Ensure client is authorized to redirect to the redirect_uri requested.

        All clients should register the absolute URIs of all URIs they intend
        to redirect to. The registration is outside of the scope of oauthlib.

        :param client_id: Unicode client identifier.
        :param redirect_uri: Unicode absolute URI.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
            - Implicit Grant
        """

        return request.client.validate_redirect_uri(redirect_uri)

    def validate_refresh_token(self, refresh_token: str, client: domain.Client, request: Request, *args, **kwargs):
        """Ensure the Bearer token is valid and authorized access to scopes.

        OBS! The request.user attribute should be set to the resource owner
        associated with this refresh token.

        :param refresh_token: Unicode refresh token.
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant (indirectly by issuing refresh tokens)
            - Resource Owner Password Credentials Grant (also indirectly)
            - Refresh Token Grant
        """

        bearer_token: domain.BearerToken
        bearer_token, _ = self._get_bearer_token(refresh_token, 'refresh_token')
        if not bearer_token:
            return False
        if bearer_token.validate_refresh_token(refresh_token, client):
            request.user = bearer_token.user
            request.old_token = bearer_token
            return True
        return False

    def validate_response_type(self, client_id: str, response_type: str, client: domain.Client, request: Request, *args, **kwargs):
        """Ensure client is authorized to use the response_type requested.

        :param client_id: Unicode client identifier.
        :param response_type: Unicode response type, i.e. code, token.
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Authorization Code Grant
            - Implicit Grant
        """

        return client.validate_response_type(response_type)

    def validate_scopes(self, client_id: str, scopes: List[str], client: domain.Client, request: Request, *args, **kwargs):
        """Ensure the client is authorized access to requested scopes.

        :param client_id: Unicode client identifier.
        :param scopes: List of scopes (defined by you).
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by all core grant types:
            - Authorization Code Grant
            - Implicit Grant
            - Resource Owner Password Credentials Grant
            - Client Credentials Grant
        """

        if hasattr(request, 'login_scopes'):
            return True
        return client.validate_scopes(scopes)

    def validate_user(self, username: str, password: str, client: domain.Client, request: Request, *args, **kwargs):
        """Ensure the username and password is valid.

        OBS! The validation should also set the user attribute of the request
        to a valid resource owner, i.e. request.user = username or similar. If
        not set you will be unable to associate a token with a user in the
        persistance method used (commonly, save_bearer_token).

        :param username: Unicode username.
        :param password: Unicode password.
        :param client: Client object set by you, see ``.authenticate_client``.
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        :rtype: True or False

        Method is used by:
            - Resource Owner Password Credentials Grant
        """
        user: domain.User = self._get_user(username)

        if not user:
            return False
        if user.correct_password(password):
            request.login_scopes = user.get_scopes()
            request.user = user
            return True
        return False

    def _get_client(self, client_id: str):
        if client_id is None:
            return None
        return self._registry(domain.Client).find(lambda x: x.client_id == client_id)

    def _get_user(self, username: str):
        return self._registry(domain.User).find(
            lambda x: ((x.email.lower() == username) | (x.preferred_username == username)) & (x.deleted_at.is_none())
        )

    def _get_bearer_token(self, token: str, token_type_hint: str = None):
        if token is None:
            return None, None
        refresh_criteria = lambda x: (x.refresh_token == token)
        access_criteria = lambda x: (x.access_token == token)

        current_token_type = 0
        criteria = [refresh_criteria, access_criteria]
        if token_type_hint == self._valid_token_type_hints[1]:
            current_token_type = 1

        bearer_token = self._registry(domain.BearerToken).find(criteria[current_token_type])
        token_type = self._valid_token_type_hints[current_token_type]

        if not bearer_token:
            current_token_type = (current_token_type + 1) % 2
            bearer_token = self._registry(domain.BearerToken).find(criteria[current_token_type])
            token_type = self._valid_token_type_hints[current_token_type]

        return bearer_token, token_type

    def _get_authorization_code(self, code: Union[str, dict, domain.AuthorizationCode]):
        code_str = code if isinstance(code, str) else code['code'] if isinstance(code, dict) else code.code
        return self._registry(domain.AuthorizationCode).find(lambda x: (x.code == code_str)) if isinstance(code_str, str) else code

    def _http_headers_authentication(self, request: Request):
        username = request.body.get('username')
        password = request.body.get('password')
        if username and password:
            user = self._registry(domain.User).find(
                lambda x: ((x.email.lower() == username) | (x.preferred_username == username)) & (x.deleted_at.is_none())
            )
            if user:
                if user.correct_password(request.body['password']):
                    client = self._registry(domain.Client).find(lambda x: x.tenant_id == user.tenant_id)
                    if not client:
                        client = self._registry(domain.Client).find(lambda x: x.client_id == user.sub)

                    if client:
                        request.client = client
                        return True
        client_secret = request.body.get('client_secret')
        client: domain.Client = self._get_client(request.client_id)

        if not client or not client_secret:
            return False
        if client.client_secret == client_secret:
            request.client = client
            return True
        return False

    def _generate_bearer_token(self, token: dict, request: Request):
        user = request.user or self._registry(domain.User).find(lambda x: ((x.tenant_id == request.client.tenant_id) | (x.sub == request.client.client_id)) & (x.deleted_at.is_none()))
        client = request.client or self._registry(domain.Client).find(lambda x: (x.tenant_id == request.user.tenant_id) | (x.client_id == request.client.client_id))
        scopes = getattr(request, 'login_scopes', request.scopes)
        return domain.BearerToken(
            client=client,
            user=user,
            scopes=self._convert_list_to_scopes(scopes),
            access_token=token['access_token'],
            expires_at=datetime.utcnow() + timedelta(seconds=token['expires_in']),
            refresh_token=token.get('refresh_token'),
            token_type=token.get('token_type'),
            claims=request.claims
        )

    def _generate_authorization_code(self, code: dict, request: Request, claims: dict):
        user = request.user or self._registry(domain.User).find(lambda x: (x.sub == self._kernel.user.id) & (x.deleted_at.is_none()))
        scopes = getattr(request, 'login_scopes', request.scopes)
        return domain.AuthorizationCode(
            client=request.client,
            user=user,
            scopes=self._convert_list_to_scopes(scopes),
            code=code['code'],
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            redirect_uri=request.redirect_uri,
            challenge=request.code_challenge,
            challenge_method='S256',
            claims=claims,
            state=code.get('state'),
            )

    def _generate_introspection_response(self, bearer_token: domain.BearerToken, token: str, token_type: str, request: Request):
        is_active = bearer_token.validate_access_token(token, request.client) if token_type == 'access_token' else bearer_token.validate_refresh_token(token, request.client)
        decoded_token = self._decode_token(token, bearer_token.client.client_id)
        resp = {
            'active': is_active,
            'scope': bearer_token.get_scopes(),
            'client_id': bearer_token.client.client_id,
            'username': bearer_token.user.email or bearer_token.user.preferred_username, #use whichever one isn't None
            'token_type': token_type,
            'exp': bearer_token.expires_at.timestamp(),
            'iat': bearer_token.created_at.timestamp(),
            'nbf': bearer_token.activates_at.timestamp(),
            'sub': bearer_token.user.sub,
            'aud': bearer_token.client.client_id,
            'iss': decoded_token['iss'],
            'jti': decoded_token['jti'],
        } if bearer_token and is_active else None

        return resp

    def _convert_list_to_scopes(self, scopes_list: list):
        scopes = []
        if isinstance(scopes_list, str) and scopes_list.startswith('['):
            for char in ('[', ']', ',', "'"):
                scopes_list = scopes_list.replace(char, '')
            scopes_list = scopes_list.split(' ')
        for s in scopes_list:
            if isinstance(s, domain.Scope):
                scopes.append(s)
            else:
                scope = self._registry(domain.Scope).find(s)
                if scope is not None:
                    scopes.append(scope)

        return scopes
