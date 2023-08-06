"""
Este módulo traz funções para autenticação em APIs.

As autenticações disponíveis até o momento são:
    - Basic Authentication
    - Digest Authentication
    - OAuth1
    - OAuth2
"""

import re
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from rauth import OAuth1Service, OAuth2Service


def auth_basic(auth_url, username, password):
    """
    Basic Authentication NÃO é recomendada, a menos que a rede seja 
    protegida por SSL (https).

    O HTTPBasicAuth já faz o encode de 'username':'password' 
    automaticamente e o passa pelo cabeçalho na chave:
        'Authorization': 'Basic <base64(username:password)>'

    Parameters
    ----------
    auth_url : string
        Endpoint de autenticação da API

    username : string
        Usuário para autenticação na API

    password : string
        Senha para autenticação na API

    Returns
    -------
    auth_header : dict
        Header HTTP para autenticação

    """
    req = requests.get(auth_url, 
                        auth=HTTPBasicAuth(username=username, 
                                            password=password))
    access_token = req.request.headers['Authorization']
    auth_header = {'Authorization': access_token}
    
    return auth_header
    # self.headers.update(auth_header)


def auth_digest(auth_url, username, password):
    """
    É preferido ao invés de Basic Authentication.

    O HTTPDigestAuth faz o encode do 'username' e 'password' e 
    acrescenta um 'nonce', criptografando-os em MD5 ao invés de Base64.
    É enviada pelo cabeçalho na chave:
        'Authorization': 'Digest <informacoes_processo_digest>'

    Parameters
    ----------
    auth_url : string
        Endpoint de autenticação da API
    
    username : string
        Usuário para autenticação na API

    password : string
        Senha para autenticação na API

    Returns
    -------
    auth_header : dict
        Header HTTP para autenticação

    """
    req = requests.get(auth_url,
                        auth=HTTPDigestAuth(username=username,
                                            password=password))
    access_token = req.request.headers['Authorization']
    auth_header = {'Authorization': access_token}
    
    return auth_header
    # self.headers.update(auth_header)


def auth_oauth1(base_url, 
                client_key, 
                client_secret, 
                request_token_url, 
                authorize_url,
                request_access_token_url):
    """
    Para autenticação por OAuth, é necessário que antes de tudo seja 
    feito um processo manual por parte do usuário, que é obter algumas 
    credenciais do cliente:
        - client_key/consumer_key
        - client_secret/consumer_secret
        - request_token_url
        - access_token_url
        - authorize_url
        - base_url

    Parameters
    ----------
    base_url : str
        URL da API sem nenhum endpoint ou argumento. É a URL base para
        as requisições.

    client_key : string
        Chave única para consumir um recurso da API

    client_secret : string
        É a "senha" que em conjunto com a client_key é usada para
        requisitar acesso à um recurso da API

    request_token_url : string
        Endpoint para requisitar um Request Token

    authorize_url : string
        Endpoint para requisitar autorização para usar o recurso.

    request_access_token_url : string
        Endpoint para requisitar o Access Token

    Returns
    -------
    session : rauth.OAuth1Service object
        Sessão autenticada com o protocolo OAuth1, pronta para receber
        requisições.

    """
    # Instanciando a sessão do OAuth1
    oauth_service = OAuth1Service(consumer_key=client_key,
        consumer_secret=client_secret,
        request_token_url=request_token_url,
        access_token_url=request_access_token_url,
        authorize_url=authorize_url,
        base_url=base_url
    )

    # Trazendo um Request Token e o Request Token Secret
    request_token, request_token_secret = (oauth_service
                                            .get_request_token())

    # Pedindo autorização do dono dos recursos para acessar
    #   os dados pela API.
    authorize_url = oauth_service.get_authorize_url(request_token)
    print('Por favor, acesse e autorize', authorize_url)

    # Pegando o verifier pela URL ou pelo PIN de acesso
    redirect_response = input('URL de redirecionamento, se não'
        ' houver deixe em branco: ')
    if redirect_response:
        verifier = (redirect_response
                    .split('oauth_verifier=',1)[1]
                    .split('#')[0])
    else:
        verifier = input('Cole o PIN de acesso: ')
    
    # Trocando os itens coletados até o momento por uma sessão autenticada
    session = oauth_service.get_auth_session(request_token,
        request_token_secret,
        method='POST',
        data={'oauth_verifier': verifier})
    
    return session


def auth_oauth2(base_url,
                client_key, 
                client_secret,
                authorize_url,
                request_access_token_url,
                redirect_uri):
    """
    Para autenticação por OAuth, é necessário que antes de tudo seja 
    feito um processo manual por parte do usuário, que é obter algumas 
    credenciais do cliente:
        - client_key/consumer_key
        - client_secret/consumer_secret
        - access_token_url
        - authorize_url
        - base_url
        - redirect_uri

    Parameters
    ----------
    base_url : str
        URL da API sem nenhum endpoint ou argumento. É a URL base para
        as requisições.
    
    client_key : string
        Chave única para consumir um recurso da API

    client_secret : string
        É a "senha" que em conjunto com a client_key é usada para
        requisitar acesso à um recurso da API

    authorize_url : string
        Endpoint para requisitar autorização para usar o recurso.

    request_access_token_url : string
        Endpoint para requisitar o Access Token
    
    redirect_uri : string
        URL para redirecionamento após autenticação e/ou autorização

    Returns
    -------
    session : rauth.OAuth2Service object
        Sessão autenticada com o protocolo OAuth1, pronta para receber
        requisições.

    """
    # Instanciando a sessão do OAuth2
    oauth_service = OAuth2Service(client_id=client_key,
        client_secret=client_secret,
        access_token_url=request_access_token_url,
        authorize_url=authorize_url,
        base_url=base_url)
    
    # Pedindo autorização do dono dos recursos para acessar
    #   os dados pela API.
    authorize_url = oauth_service.get_authorize_url()
    print('Por favor, acesse e autorize', authorize_url)

    # Pegando o code pela URL
    url_with_code = input('URL de redirecionamento: ')
    code = re.search('\?code=([^&]*)', url_with_code).group(1)

    # Montando um cabeçalho com os dados da URL e code
    data = {'code': code, 'redirect_uri': redirect_uri}

    # Trocando os itens coletados até o momento por uma sessão autenticada
    session = oauth_service.get_auth_session(data=data)
    
    return session


def auth_oauth2_salesforce(request_access_token_url,
                            client_key,
                            client_secret,
                            username,
                            password):
    """
    Para autenticação por OAuth no Salesforce, é necessário que antes de 
    tudo seja feito um processo manual por parte do usuário, que é obter 
    algumas credenciais do cliente:
        - client_key/consumer_key
        - client_secret/consumer_secret
        - request_access_token_url
        - username
        - password
        - security_token

    Parameters
    ----------
    request_access_token_url : string
        Endpoint para requisitar o Access Token
    
    client_key : string
        Chave única para consumir um recurso da API

    client_secret : string
        É a "senha" que em conjunto com a client_key é usada para
        requisitar acesso à um recurso da API
    
    username : string
        Usuário para autenticação na API

    password : string
        Senha para autenticação na API. A senha é composto pela própria
        senha e por um security_token, que pode ser gerado no ambiente 
        de Configurações da conta do Salesforce: 
            <password><security_token>
    
    """
    # Instanciando o objeto requests.Response
    response = requests.post(request_access_token_url, 
        data = {'client_id': client_key,
        'client_secret': client_secret,
        'grant_type': 'password',
        'username': username,
        'password': password}
    )

    # Pegando o Access Token
    json_response = response.json()
    access_token = json_response['access_token']
    auth_header = {'Authorization': 'Bearer ' + access_token}

    # Reafirmando a URL de acesso
    instance_url = json_response['instance_url']

    return instance_url, auth_header