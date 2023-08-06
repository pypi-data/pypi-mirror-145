import jwt
from typing import Union


def _get_token(secret: str = 'secret') -> str:
    # make sure the user matches the db_state.sql
    token_data = {
        "datalake": {
            "user_id": "68eda64b-f933-473b-b3ef-4d8e22baa648",
            "organisation_id": "9516c0ba-ba7e-11e9-8b34-000c6c0a981f"
        },
        "name": "w molicki",
        "email": "wmolicki@qa.com",
        "sub": "wmolicki@qa.com",
        "azp": "datalake-catalogue-dev",
        "aud": "datalake-catalogue-dev",
        "iat": 1624958089,
        "exp": 1656580489
    }

    token_encoded: Union[str, bytes] = jwt.encode(token_data, secret)
    if isinstance(token_encoded, bytes):
        return token_encoded.decode('utf-8')
    else:
        return token_encoded

