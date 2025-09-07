import yaml, re
from pathlib import Path
from jsonschema import validate, ValidationError

BASIC_OAS_SCHEMA = {'type':'object','properties':{'openapi':{'type':'string'},'info':{'type':'object'},'paths':{'type':'object'}},'required':['openapi','info','paths']}
PII_HINTS = re.compile(r'(ssn|email|phone|dob|address|pan|card|cc|crn|aadhaar)', re.I)

def discover_oas(workspace_root: str, globs_pattern=None):
    from pathlib import Path
    patterns = globs_pattern or ['**/openapi.yaml','**/openapi.yml','**/openapi.json']
    root = Path(workspace_root)
    matches = []
    for pat in patterns: matches += [str(p) for p in root.glob(pat)]
    return {'oasPaths': sorted(matches)}

def load_oas(path: str):
    p = Path(path); data = yaml.safe_load(p.read_text())
    try: validate(data, BASIC_OAS_SCHEMA)
    except ValidationError as e: raise ValueError(f'Basic OpenAPI shape invalid: {e.message}')
    return data

def _scan_schemas_for_pii(components):
    hints=[]; 
    if not components: return hints
    schemas = components.get('schemas', {})
    for name, schema in schemas.items():
        props = schema.get('properties', {}) if isinstance(schema, dict) else {}
        for prop in props:
            if PII_HINTS.search(prop): hints.append({'schema': name, 'field': prop})
    return hints

def extract_traits(spec: dict):
    paths=spec.get('paths', {}); methods=0; max_body_bytes=0; public_exposure=True
    for path, ops in paths.items():
        for m, op in ops.items():
            if m.lower() in {'get','post','put','delete','patch','options','head'}:
                methods+=1
                rb=op.get('requestBody', {}); content=rb.get('content', {}) if isinstance(rb, dict) else {}
                for mt, media in content.items():
                    ex = media.get('example') or (media.get('examples', {}).get('default', {}) if isinstance(media.get('examples'), dict) else None)
                    if isinstance(ex, (str, bytes)): max_body_bytes=max(max_body_bytes, len(str(ex).encode()))
                if op.get('x-internal') is True: public_exposure=False
    pii_hits = _scan_schemas_for_pii(spec.get('components'))
    has_pci = any(h for h in pii_hits if re.search(r'(card|pan|crn|cc)', h['field'], re.I))
    return {'summary': {'endpoints': len(paths), 'operations': methods, 'public': public_exposure, 'max_body_bytes_hint': max_body_bytes},
            'data_signals': {'pii_fields': pii_hits, 'pci_suspected': has_pci}}
