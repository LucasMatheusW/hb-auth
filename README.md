HBAuth
=====

Authenticador centralizado para os Sites HB

Quick start - DEVELOPMENT
-----------

1. Crie um ambiente virtual com ``python -m venv env`` e ative ele com ``.\env\Scripts\activate``::

2. Execute ``pip install -r requirements.txt`` para instalar as dependências::

3. Para gerar uma release nova, abra um PR para a main, quando for aprovado e feito merge basta executar um novo deploy::

Quick start - USAGE as AUTHPROVIDER
-----------

1. Execute o comando ``python manage.py migrate`` para aplicar a migration.

2. Execute o comando ``python manage.py runserver`` para executar a aplicação.

Quick start - USAGE in CONSUMER
-----------

1. Crie uma application nova no admin do Django

2. Guarde a ClientID e a ClientSecret

3. Faça a seguinte configuração::
```python
    SOCIAL_AUTH_HANNABANANNA_KEY = "<your_key>"
    SOCIAL_AUTH_HANNABANANNA_SECRET = "<your_secret>"

    HANNABANNA_AUTH_URL = "<your_hbauth_backend>"
```

4. Execute o comando ``python manage.py runserver`` para executar a aplicação do client.

5. Utilize a autenticação pelo template com a tag ``{% url "social:begin "hannabananna" %}``<br><sub><sup>(A namespace 'social' é importada do pacote ``python-social-auth``)</sup></sub>

6. Para utilizar a autenticação pelo DRFaça uma requisição POST para o seu client na URL de acess com o body:
```json
{
    "provider": "hannabananna -- se o seu backend utilizar rest-social-auth",
    "code": "<codigo de autorização que retornou da api de authorize do HBAuth>"
}
```
Esse REST irá retornar um access token que pode ser trocado por um access token da aplicação client.