#!/usr/bin/env python3
"""Serve out/ like Vercel static hosting for local verification:
- /path/ -> out/path/index.html
- /path  -> out/path.html if it exists, else out/path/index.html
- /      -> out/index.html
"""
import http.server, os, sys, functools
OUT = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site/out')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8317

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=OUT, **kw)
    def translate_path(self, path):
        p = super().translate_path(path)
        if os.path.isdir(p):
            return os.path.join(p, 'index.html')
        if not os.path.exists(p):
            if os.path.exists(p + '.html'):
                return p + '.html'
            idx = os.path.join(p, 'index.html')
            if os.path.exists(idx):
                return idx
        return p
    def log_message(self, *a):
        pass

http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
