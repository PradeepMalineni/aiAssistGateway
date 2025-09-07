#!/usr/bin/env python3
import argparse, csv, os, re
from pathlib import Path
def slugify(path: str) -> str:
    import re
    s = re.sub(r'[^a-zA-Z0-9\-_/\.]', '-', path).replace('\\','/')
    s = re.sub(r'\.md$', '', s).strip('/')
    parts = s.split('/'); key = parts[-1] if len(parts[-1])>1 else '-'.join(parts)
    return key.lower()
def scan_docs(d): 
    r=Path(d)
    for p in r.rglob('*.md'): yield p.relative_to(r).as_posix()
def build_index(repo_url, branch, docs_dir, llm='Y', link_prefix=''):
    rows=[]
    for rel in scan_docs(docs_dir):
        topic=slugify(rel); fp=f'/{Path(docs_dir).as_posix()}/{rel}'
        link=f'{link_prefix}{fp}' if link_prefix else ''
        rows.append([topic, repo_url, branch, fp, llm.upper(), link])
    return sorted(rows, key=lambda r: r[0])
def write_index(rows, out_csv):
    Path(out_csv).write_text('\n'.join([','.join(map(str,r)) for r in rows])+'\n')
def write_prompt(rows, out_md):
    with open(out_md,'w',encoding='utf-8') as f:
        f.write('# DevX Prompt Map\n\n')
        for topic,*_ in rows:
            f.write(f'Query: Anything related to {topic.replace(\"-\",\" \")}\n')
            f.write(f'Respond: {topic}\n\n')
        f.write('Query: Decide the right API gateway for my service\nRespond: gateway-assistant\n\n')
        f.write('Query: Generate proxy bundle from my OAS with security guardrails\nRespond: gateway-assistant\n\n')
if __name__=='__main__':
    import argparse; ap=argparse.ArgumentParser()
    ap.add_argument('--repo-url', required=True); ap.add_argument('--branch', default='main')
    ap.add_argument('--docs-dir', default='docs'); ap.add_argument('--out-csv', default='index.csv')
    ap.add_argument('--out-prompt', default='prompt.md'); ap.add_argument('--llm', default='Y')
    ap.add_argument('--link-prefix', default='')
    a=ap.parse_args(); rows=build_index(a.repo_url,a.branch,a.docs_dir,a.llm,a.link_prefix)
    write_index(rows, a.out_csv); write_prompt(rows, a.out_prompt)
    print(f'Wrote {a.out_csv} and {a.out_prompt}. {len(rows)} topics discovered.')
