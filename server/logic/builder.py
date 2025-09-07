from pathlib import Path
import yaml, json
from jinja2 import Environment, FileSystemLoader
def generate_bundle(spec: dict, plan: dict, out_dir: str, decision: dict):
    out=Path(out_dir); (out / 'apigee/bundle/policies').mkdir(parents=True, exist_ok=True); (out / 'datapower').mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(Path(__file__).parent.parent / 'templates')))
    artifacts=[]; applied_controls=plan['required_controls'][:]
    (out/'guardrail_plan.yaml').write_text(yaml.safe_dump(plan, sort_keys=False)); artifacts.append(str(out/'guardrail_plan.yaml'))
    (out/'decision.json').write_text(json.dumps(decision, indent=2)); artifacts.append(str(out/'decision.json'))
    (out/'compliance_report.md').write_text('\n'.join(['# Compliance Report','','- Required controls: '+', '.join(plan['required_controls']), f"- Decision: {decision['gateway']}"])) ; artifacts.append(str(out/'compliance_report.md'))
    if decision['gateway']=='apigee':
        proxy_tpl=env.get_template('apigee/proxy.xml.j2'); (out/'apigee/bundle/proxy.xml').write_text(proxy_tpl.render(name='AI-Generated-Proxy')); artifacts.append(str(out/'apigee/bundle/proxy.xml'))
        if 'spike-arrest' in plan['required_controls']:
            spike_tpl=env.get_template('apigee/policies/SpikeArrest.xml.j2'); (out/'apigee/bundle/policies/SpikeArrest.xml').write_text(spike_tpl.render(name='Spike-Arrest-1', rate=f"{plan['thresholds']['rate_limit_per_app_per_min']}pm")); artifacts.append(str(out/'apigee/bundle/policies/SpikeArrest.xml'))
        if 'oauth-jwt' in plan['required_controls']:
            oauth_tpl=env.get_template('apigee/policies/OAuthV2.xml.j2'); (out/'apigee/bundle/policies/OAuthV2.xml').write_text(oauth_tpl.render(name='OAuthV2-Verify', operation='VerifyJWT')); artifacts.append(str(out/'apigee/bundle/policies/OAuthV2.xml'))
    else:
        dp_tpl=env.get_template('datapower/config.xml.j2'); (out/'datapower/config.xml').write_text(dp_tpl.render(name='AI-Generated-Service')); artifacts.append(str(out/'datapower/config.xml'))
    return {'artifacts': artifacts, 'applied_controls': applied_controls}
