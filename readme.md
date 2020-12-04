# InsomniaAPI

Simple API, which contains endpoint which returns balance for specified TRX addresses. Balance endpoint has simple API-Key authorization.

## Endpoints

- `/hc` - **Healthcheck** endpoint retrieves data about overall health of API.
- `/your-trx-address` - **Balance** endpoint shows balance amount on provided trx address.

## Authorization

Any request to balance endpoint must contain `Authorization` header, which contains API key.

## Requirements

- python 3.7 or greater
- virtualenv

## How to run

Clone repository, create your own `config.json` file, in root. You can use `config.json.example` file as a template. Afterwards just run following command:

`./run.sh`

For dev purposes run:

`./run.sh dev`

## Example Curls

```bash
curl http://127.0.0.1:5000/hc

curl http://127.0.0.1:5000/4101e67b5bf421688148e2c6e9be6fbd74687658dd

curl http://127.0.0.1:5000/4101e67b5bf421688148e2c6e9be6fbd74687658dd -H "Authorization: 4rFP8aBhjq8Ih5l1sZUER9TBWO8yGkZKlJLgnTNT"
```