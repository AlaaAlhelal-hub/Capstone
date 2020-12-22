import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# AUTH0 Configuration
AUTH0_DOMAIN = 'alaa-fsnd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'CoffeeShop'


## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def verify_decode_jwt(token):
    # verify the token using Auth0 /.well-known/jwks.json
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    #it should be an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }


    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            #decode the payload from the token
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            #return the decoded payload
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        #no header is present
        raise AuthError({
        'error': 'header_missing',
        'description': 'No Authorization header supplied'
        }, 401)

    auth_header = request.headers['Authorization']
    header_part = auth_header.split(' ')

    if len(header_part) != 2:
        raise AuthError({
        'error': 'invalid__auth_header',
        'description': 'Invalid token supplied.'
        }, 401)

    elif header_part[0].lower() != 'bearer':
        raise AuthError({
        'error': 'invalid__auth_header',
        'description': 'Invalid token supplied. Bearer token expected'
        }, 401)

    #return the token part of the header
    return header_part[1]



def check_permissions(permission, payload):
    if 'permissions' not in payload :
        raise AuthError({
        'code': 'invalid_claims',
        'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
        'code': 'unauthorized',
        'description': 'Permission not found.'
        }, 403)

    return True



def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
