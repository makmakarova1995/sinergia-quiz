#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проставляет ?v=<хеш> к путям картинок в offers.html и offers-emba.html.
Запускать после каждой замены файлов в creo/:  python3 bust.py
"""
import hashlib, re, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = [os.path.join(ROOT, f) for f in ('offers.html', 'offers-emba.html')]

def h(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

for PAGE in PAGES:
    if not os.path.exists(PAGE):
        continue
    s = open(PAGE, encoding='utf-8').read()
    n = 0
    def sub(m):
        global n
        rel = m.group(1)
        full = os.path.join(ROOT, rel)
        if not os.path.exists(full):
            print('нет файла:', rel); return m.group(0)
        n += 1
        return 'data-creo="%s?v=%s"' % (rel, h(full))
    s = re.sub(r'data-creo="(creo/[^"?]+)(?:\?v=[0-9a-f]+)?"', sub, s)
    open(PAGE, 'w', encoding='utf-8').write(s)
    print(os.path.basename(PAGE), '— обновлено версий:', n)
