import yaml
from pathlib import Path
CATALOG_PATH = Path(__file__).parent.parent / 'policy' / 'policy_catalog.yaml'
def plan_from_traits(traits: dict, use_llm: bool=False, model=None) -> dict:
    catalog = yaml.safe_load(CATALOG_PATH.read_text())
    required=set(['fault-handling','schema-validate-req','schema-validate-res','spike-arrest'])
    required |= set(['oauth-jwt','tls12+','hsts']) if traits['summary']['public'] else set(['mtls','jwt-optional'])
    if traits['data_signals'].get('pci_suspected'): required |= set(['dlp-tokenize','field-mask','no-logging-sensitive'])
    plan={'required_controls': sorted(list(required)),
          'rationale': {'public': traits['summary']['public'], 'pci_suspected': traits['data_signals'].get('pci_suspected', False)},
          'thresholds': {'rate_limit_per_app_per_min': traits.get('thresholds',{}).get('rate_limit_per_app_per_min', 600), 'max_body_bytes': max(1024*1024, traits['summary']['max_body_bytes_hint'] or 0)}}
    return plan
