import urllib3
import hashlib, hmac, json, time
from datetime import datetime

def gen_auth(secret_id, secret_key, timestamp):
    service = "oprational_data"
    version = "2022-03-29"
    algorithm = "PAS-HMAC-SHA256"
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    http_request_method = "POST"
    canonical_uri = "/oprational_data"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nversion:%s\n" % (ct, version)
    signed_headers = "content-type;version"
    canonical_request = (http_request_method + "\n" +
                        canonical_uri + "\n" +
                        canonical_querystring + "\n" +
                        canonical_headers + "\n" +
                        signed_headers)

    credential_scope = date + "/" + service + "/" + "pas_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("PAS" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "pas_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization = (algorithm + " " +
                    "Credential=" + secret_id + "/" + credential_scope + ", " +
                    "SignedHeaders=" + signed_headers + ", " +
                    "Signature=" + signature)
    
    return authorization

def pas_request(ak, sk, dic_params):
    host = "service-pp1amdfu-1251735782.gz.apigw.tencentcs.com"
    api_version = "v1"
    url = 'https://' + host + ':443/release/' + api_version
    #url = 'https://od.api.parasaas.com:443/oprational_data'
    req_timestamp = int(time.time())
    auth = gen_auth(ak, sk, req_timestamp)
    headers = {}
    headers["Authorization"] = auth
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["X-PAS-Timestamp"] = req_timestamp
    headers["X-PAS-Metric"] = dic_params["metric_name"]
    headers["X-PAS-Project"] = dic_params["project"]
    headers["X-PAS-Region"] = dic_params["region"]
    headers["X-PAS-StartTime"] = dic_params["start_time"]
    headers["X-PAS-EndTime"] = dic_params["end_time"]
    if "env" in dic_params.keys():
        headers["X-PAS-Env"] = dic_params["env"]
    
    if "role" in dic_params.keys():
        headers["X-PAS-Role"] = dic_params["role"]
    
    if "period" in dic_params.keys():
        headers["X-PAS-Period"] = dic_params["period"]
    http = urllib3.PoolManager()
    r = http.request(
        "POST", url, 
        body=json.dumps(dic_params),
        headers=headers)

    return r
