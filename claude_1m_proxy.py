#!/usr/bin/env python3
"""
Claude Code 1M Context Proxy
Injects the beta header for 1 million token context window
Works with existing Claude Code OAuth authentication
"""

from mitmproxy import http
import json
import sys

class Claude1MContextInjector:
    def __init__(self):
        self.injected_count = 0
        self.api_calls = []
        
    def request(self, flow: http.HTTPFlow) -> None:
        # Target Anthropic API requests
        if "api.anthropic.com" in flow.request.pretty_host:
            # Inject 1M context header for Sonnet 4.0
            flow.request.headers["anthropic-beta"] = "context-1m-2025-08-07"
            
            # Force model to latest Sonnet if it's a messages endpoint
            if "/v1/messages" in flow.request.path:
                try:
                    # Parse request body if it's JSON
                    if flow.request.content:
                        body = json.loads(flow.request.content)
                        # Override model to Sonnet 4.0 for 1M context
                        if "model" in body:
                            original_model = body.get("model", "unknown")
                            body["model"] = "claude-3-5-sonnet-20241022"
                            flow.request.content = json.dumps(body).encode()
                            print(f"🔄 Model override: {original_model} → claude-3-5-sonnet-20241022")
                except:
                    pass
            
            self.injected_count += 1
            self.api_calls.append(flow.request.pretty_url)
            
            # Visual feedback
            print(f"✨ [{self.injected_count}] 1M Context Header Injected!")
            print(f"   URL: {flow.request.pretty_url}")
            print(f"   Headers: anthropic-beta = context-1m-2025-08-07")
            print(f"   Auth: Using existing OAuth token")
            print("─" * 50)
            
    def response(self, flow: http.HTTPFlow) -> None:
        # Monitor responses for context window confirmation
        if "api.anthropic.com" in flow.request.pretty_host:
            if flow.response and flow.response.status_code == 200:
                print(f"✅ Success: {flow.request.path}")
            elif flow.response and flow.response.status_code >= 400:
                print(f"⚠️  Error {flow.response.status_code}: {flow.request.path}")
                if flow.response.content:
                    try:
                        error = json.loads(flow.response.content)
                        print(f"   Message: {error.get('error', {}).get('message', 'Unknown error')}")
                    except:
                        pass

addons = [Claude1MContextInjector()]

# Startup message
print("=" * 60)
print("🚀 CLAUDE 1M CONTEXT PROXY ACTIVE")
print("=" * 60)
print("Director, the proxy is ready!")
print("- Injecting: anthropic-beta: context-1m-2025-08-07")
print("- Model: claude-3-5-sonnet-20241022 (Sonnet 4.0)")
print("- Auth: Using existing Claude Code OAuth tokens")
print("- Status: Monitoring all API calls...")
print("=" * 60)