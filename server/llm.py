import os, json
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt
def _client(): return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
@retry(wait=wait_exponential(min=1, max=20), stop=stop_after_attempt(3))
def _json_call(messages, model=None):
    client=_client()
    resp=client.chat.completions.create(model=model or 'gpt-4.1-mini', messages=messages, temperature=0, response_format={'type':'json_object'})
    return json.loads(resp.choices[0].message.content)
def merge_llm_traits(spec: dict, traits: dict, model=None) -> dict:
    spec_text=json.dumps(spec)[:120000]
    sys='Return compact JSON: public(bool), pci_suspected(bool), pii_signals([{schema,field}]), suggested_rate_per_app_min(int).'
    msg=[{'role':'system','content':sys},{'role':'user','content':spec_text}]
    llm=_json_call(msg, model=model)
    merged=traits.copy()
    if 'public' in llm: merged['summary']['public']=bool(llm['public'])
    if 'pci_suspected' in llm: merged['data_signals']['pci_suspected']=bool(llm['pci_suspected'])
    if 'pii_signals' in llm: merged['data_signals']['pii_fields']=llm['pii_signals']
    if 'suggested_rate_per_app_min' in llm: merged.setdefault('thresholds',{})['rate_limit_per_app_per_min']=int(llm['suggested_rate_per_app_min'])
    return merged
