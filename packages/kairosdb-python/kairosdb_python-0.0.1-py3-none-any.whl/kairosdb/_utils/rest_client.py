from kairosdb._cnsts import SUCCESS_CODES
from kairosdb.errors import MODULE_NOT_FOUND_MSG, ApiCallError

try:
    import httpx
except ImportError:
    raise ModuleNotFoundError(f"{MODULE_NOT_FOUND_MSG}: httpx")


def post(url: str, json: dict = None, data=None, headers: dict | None = None) -> httpx.Response:
    with httpx.Client() as client:
        r = client.post(
            url=url,
            json=json,
            data=data,
            headers=headers
        )
        if r.status_code not in SUCCESS_CODES:
            raise ApiCallError(
                f"API Call failed. Server responded with status code: {r.status_code}",
                details=r.json()
            )
        return r


def get(url: str, headers: dict = None) -> httpx.Response:
    with httpx.Client() as client:
        r = client.get(
            url=url,
            headers=headers
        )
        if r.status_code not in SUCCESS_CODES:
            raise ApiCallError
        return r
