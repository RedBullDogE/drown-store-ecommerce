# Drown Store project
Store app writen using:
* Django + gunicorn
* Postgresql
* Nginx
* Docker
* Stripe as a payment system

[MDB templates](https://mdbootstrap.com/docs/b4/jquery/templates/ecommerence/) were used for layout.

## Setup
To set up this project on your machine you should clone this repo, add .env with specific settings to the project root and setup certificates for using HTTPS. Then project should work fine. 

Optionally, you can also change django, nginx or docker settings in the corresponding configuration files.

For build and start project you should `run docker-compose up -d --build`

### Env variables

|   Variable    |   value   |
|---------------|-----------|
| ENVIROMENT    | production/development|
| SECRET_KEY    | django secret key |
| STRIPE_SECRET_KEY | Stripe secret key |
| ALLOWED_HOSTS | domain names or IP addresses splitted by space |
| EMAIL_HOST_USER | Username of your email account, which will be used as mail sender |
| EMAIL_HOST_PASSWORD | Password of your email account |

Also you should specify in your .env file settings for Postgresql: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB (name of your database), POSTGRES_HOST, POSTGRES_PORT.