from typing import Any, Dict, Optional

import aiohttp
import datetime
import hashlib
import hmac
import urllib.parse

from cenao.app import AppFeature


class S3Client:
    _endpoint: str
    _region: str
    _bucket: str
    _access: str
    _secret: str
    _session: aiohttp.ClientSession

    def __init__(self, endpoint: str, region: str, bucket: str, access: str, secret: str):
        self._endpoint = endpoint
        self._region = region
        self._bucket = bucket
        self._access = access
        self._secret = secret

        self._session = aiohttp.ClientSession()

    async def upload_data(self, key: str, payload: bytes):
        path = f'/{self._bucket}/{key}'
        headers = self._sign(path=path, method='PUT', payload=payload)
        resp = await self._session.put(url=f'https://{self._endpoint}{path}', headers=headers, data=payload)
        resp.raise_for_status()

    def _sign(
        self,
        path: str,
        method: str,
        payload: bytes,
        headers: Optional[Dict[str, Any]] = None,
        query: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        if headers is None:
            headers = {}

        if query is None:
            query = {}

        now = datetime.datetime.utcnow()
        amzdate = now.strftime('%Y%m%dT%H%M%SZ')
        datestamp = now.strftime('%Y%m%d')
        payload_hash = hashlib.sha256(payload).hexdigest()
        credential_scope = f'{datestamp}/{self._region}/s3/aws4_request'

        headers_lower = {
            header_key.lower(): ' '.join(header_value.split())
            for header_key, header_value in headers.items()
        }

        _headers = {
            'host': self._endpoint,
            'x-amz-content-sha256': payload_hash,
            'x-amz-date': amzdate,
            **headers_lower,
        }
        header_keys = sorted(_headers.keys())
        signed_headers = ';'.join(header_keys)

        def signature():
            def canonical_request():
                canonical_uri = urllib.parse.quote(path, safe='/~')
                quoted_query = sorted(
                    (urllib.parse.quote(key, safe='~'), urllib.parse.quote(value, safe='~'))
                    for key, value in query.items()
                )
                canonical_querystring = '&'.join(f'{key}={value}' for key, value in quoted_query)
                canonical_headers = ''.join(f'{key}:{_headers[key]}\n' for key in header_keys)

                return f'{method}\n{canonical_uri}\n{canonical_querystring}\n' + \
                       f'{canonical_headers}\n{signed_headers}\n{payload_hash}'

            def sign(key, msg):
                return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

            string_to_sign = f'AWS4-HMAC-SHA256\n{amzdate}\n{credential_scope}\n' + \
                             hashlib.sha256(canonical_request().encode('utf-8')).hexdigest()

            date_key = sign(('AWS4' + self._secret).encode('utf-8'), datestamp)
            region_key = sign(date_key, self._region)
            service_key = sign(region_key, 's3')
            request_key = sign(service_key, 'aws4_request')
            return sign(request_key, string_to_sign).hex()
        return {
            **headers,
            'x-amz-date': amzdate,
            'x-amz-content-sha256': payload_hash,
            'Authorization': f'AWS4-HMAC-SHA256 Credential={self._access}/{credential_scope}, '
                             f'SignedHeaders={signed_headers}, Signature=' + signature(),
        }

    async def close(self):
        if self._session:
            await self._session.close()


class S3AppFeature(AppFeature):
    NAME = 's3'

    client: S3Client

    async def on_startup(self):
        self.client = S3Client(
            endpoint=self.config.get('endpoint'),
            region=self.config.get('region', 'us-east-1'),
            bucket=self.config.get('bucket'),
            access=self.config.get('access'),
            secret=self.config.get('secret'),
        )

    async def on_shutdown(self):
        if self.client:
            await self.client.close()
