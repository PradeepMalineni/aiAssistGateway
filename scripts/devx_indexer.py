#!/usr/bin/env python3
import argparse, csv, os, re
from pathlib import Path

def slugify(path: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9\-_/\.]', '-', path)
    s = s.replace('\\', '/')
    s = re.sub(r'\.md$', '', s)
    s = s.strip('/')
    parts = s.split('/')
    key = parts[-1] if len(parts[-1]) > 1 else '-'.join(parts)
    return key.lower()

def scan_docs(docs_dir: str):
    root = Path(docs_dir)
    for p in root.rglob('*.md'):
        rel = p.relative_to(root).as_posix()
        yield rel

def build_index(repo_url: str, branch: str, docs_dir: str, llm_default: str='Y', link_prefix: str=''):
    rows = []
    for rel in scan_docs(docs_dir):
        topic = slugify(rel)
        file_path = f"/{Path(docs_dir).as_posix()}/{rel}"
        link = f"{link_prefix}{file_path}" if link_prefix else ''
        rows.append([topic, repo_url, branch, file_path, llm_default.upper(), link])
    return sorted(rows, key=lambda r: r[0])

def write_index(rows, out_csv: str):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)

def write_prompt(rows, out_md: str):
    Path(out_md).parent.mkdir(parents=True, exist_ok=True)
    with open(out_md, 'w', encoding='utf-8') as f:
        f.write('# DevX Prompt Map\n\n')
        f.write("Use the following Query → Respond pairs. 'Respond' must match the Topic key in index.csv.\n\n")
        # docs topics
        for topic, *_ in rows:
            f.write(f"Query: Anything related to {topic.replace('-', ' ')}\n")
            f.write(f"Respond: {topic}\n\n")
        # action topic for gateway assistant
        f.write("Query: Decide the right API gateway for my service\n")
        f.write("Respond: gateway-assistant\n\n")
        f.write("Query: Generate proxy bundle from my OAS with security guardrails\n")
        f.write("Respond: gateway-assistant\n\n")

def main():
    ap = argparse.ArgumentParser(description='Generate DevX index.csv and prompt.md from docs folder')
    ap.add_argument('--repo-url', required=True, help='Git repo URL')
    ap.add_argument('--branch', default='main')
    ap.add_argument('--docs-dir', default='docs')
    ap.add_argument('--out-csv', default='index.csv')
    ap.add_argument('--out-prompt', default='prompt.md')
    ap.add_argument('--llm', default='Y', choices=['Y','N'])
    ap.add_argument('--link-prefix', default='', help='Optional absolute URL prefix for Links column')
    args = ap.parse_args()

    rows = build_index(args.repo_url, args.branch, args.docs_dir, args.llm, args.link_prefix)
    write_index(rows, args.out_csv)
    write_prompt(rows, args.out_prompt)
    print(f'Wrote {args.out_csv} and {args.out_prompt}. {len(rows)} topics discovered.')

if __name__ == '__main__':
    main()
