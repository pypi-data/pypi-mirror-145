"""
Este módulo implementa a aplicação.
"""

from . import utils


class SetupAPI(object):
    """
    Configura os parâmetros para a API que será utilizada.

    Attributes
    -----------
    base_url : string
        URL da API sem nenhum endpoint ou argumento.
    headers : string
        Cabeçalho com parâmetros para as requisições HTTP.
    version : string
        Versão da API, normalmente 'vX.X' ou 'vX'. Ex: v1, v1.3

    Methods
    -------
    config_header(self, **kwargs):
        Configura o Header HTTP para as requisições pela API.
    build_url(self, version='v1', endpoint=''):
        Monta a URL que será usada para a requisição à API.
    info(self):
        Resume as informações da API configurada.
    """

    def config_header(self, header=None,**kwargs):
        """
        Configura o Header HTTP para as requisições pela API.
        Ao invés de informar valores com '-', informe com '_'.
        Será feito o parse e substituição pelo '-' no método.

        Parameters
        ----------
        header : dict
            Dicionário com HTTP Header já definido e que precisa ser
            adicionado ao atributo headers do objeto da API. 

        **kwargs
            Parâmetros de chave-valor arbitrários. A chave deve
            ser passada sem aspas e o valor com aspas se for string.

        Returns
        -------
        headers : str
            Headers configurados para a API.
        """
        if kwargs:
            headers = {
                (key.replace('_', '-') if '_' in key else key) : value 
                for key, value in kwargs.items()
            }
        if header:
            headers = header
        self.headers.update(headers)

    def build_url(self, *args):
        """
        Monta a URL que será usada para a requisição à API.

        Parameters
        ----------
        *args : list
            Podem ser passados itens que complementem a Base URL de 
            forma a criar a URL para consumo do recurso. Ex: 
                - endpoints: usuario; area/departamento; etc.
                - version: v1; v2.3; v54.0; etc.
            Podem ser passados juntos como "v1/area/departamento" ou 
            separados como "v1", "area", "departamento".

        Returns
        -------
        url : string
            URL final que será usada na requisição.
        """
        url = self.base_url + '/'.join(args)
        self.endpoints.append(url.split(self.base_url)[1])
        return url

    def __repr__(self) -> str:
        return utils.prettify_json(vars(self))

    def __init__(self, base_url,
                    accept='*/*', 
                    accept_encoding='gzip, deflate, br', 
                    connection='keep-alive'):
        """
        Construtor da classe

        Parameters
        ----------
        base_url : string
            URL da API sem nenhum endpoint ou argumento.
        accept : string
            Indica qual tipo de conteúdo o cliente consegue entender. É 
            enviado pelo cliente para o servidor.
        accept_encoding : string
            Indica qual codificação de conteúdo o cliente está apto a 
            entender.
        connection : string
            Controla se a conexão se mantém aberta ou não após o fim da 
            transação atual.
        headers : dict
            Dicionário contendo pares chave-valor com os itens que
            serão enviados pelo cabeçalho HTTP nas requisições.
        """
        if not base_url.endswith('/'):
            self.base_url = base_url + '/'
        else:
            self.base_url = base_url

        self.endpoints = []

        self.headers = {}
        self.config_header(Accept=accept, 
                            Accept_Encoding=accept_encoding,
                            Connection=connection)
