import hashlib
import time


def make_credential_http_header(appId, secret):
    now = time.time()
    ts = int(round(now * 1000))
    sig = str(ts) + secret
    return {"luban_api_client": appId,"luban_api_ts": ts, "luban_api_signature": hashlib.sha256(sig.encode("utf-8")).hexdigest()}


def main():
    result = make_credential_http_header("web", "0bcb002c-8906-4465-b9b7-8d47d3984b1f")
    print(result)


if __name__ == '__main__':
    main()