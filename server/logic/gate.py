def evaluate(plan: dict, applied_controls: list):
    required=set(plan.get('required_controls', [])); applied=set(applied_controls or [])
    missing=sorted(list(required - applied))
    return {'pass': len(missing)==0, 'missing': missing}
