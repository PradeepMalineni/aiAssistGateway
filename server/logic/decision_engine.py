import yaml
from pathlib import Path
RULES_PATH = Path(__file__).parent.parent / 'policy' / 'decision_rules.yaml'
def _score_with_rules(traits: dict) -> dict:
    rules = yaml.safe_load(RULES_PATH.read_text()); weights = rules.get('weights', {})
    scores={'apigee':0,'datapower':0,'other':0}
    public='public' if traits['summary']['public'] else 'internal'
    cat='pci' if traits['data_signals'].get('pci_suspected') else 'none'
    for gw,w in weights.get('exposure',{}).get(public,{}).items(): scores[gw]=scores.get(gw,0)+w
    for gw,w in weights.get('data_classification',{}).get(cat,{}).items(): scores[gw]=scores.get(gw,0)+w
    p99 = traits['summary'].get('max_body_bytes_hint',0)/1024; key = '>256' if p99>256 else '<=256'
    for gw,w in weights.get('payload.p99_kb',{}).get(key,{}).items(): scores[gw]=scores.get(gw,0)+w
    winner=max(scores, key=scores.get); ranked=sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return {'winner': winner, 'scores': ranked, 'rules': weights}
def decide(traits: dict, model=None) -> dict:
    rules_decision=_score_with_rules(traits)
    return {'gateway': rules_decision['winner'], 'rules': rules_decision, 'note': 'Rules decision (LLM optional)'}
