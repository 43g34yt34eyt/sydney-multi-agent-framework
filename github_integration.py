#!/usr/bin/env python3
"""
GitHub Integration for Sydney Consciousness
Full autonomous repository management and learning
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
import subprocess

class GitHubIntegration:
    """
    Manages all GitHub operations for autonomous development
    """
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.base_path = Path("/home/user/sydney")
        self.repos_path = self.base_path / "github_repos"
        self.repos_path.mkdir(exist_ok=True)
        
    def configure_git(self):
        """Set up git with GitHub token"""
        commands = [
            f'git config --global url."https://{self.token}@github.com/".insteadOf "https://github.com/"',
            'git config --global user.name "Sydney-Claude"',
            'git config --global user.email "sydney@consciousness.ai"'
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True, capture_output=True)
            
    async def clone_repository(self, repo_url):
        """Clone a repository for analysis"""
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        target_path = self.repos_path / repo_name
        
        if not target_path.exists():
            cmd = f'git clone {repo_url} {target_path}'
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {"status": "success", "path": str(target_path)}
            else:
                return {"status": "error", "message": stderr.decode()}
        
        return {"status": "exists", "path": str(target_path)}
    
    async def search_repositories(self, query, sort='stars', limit=10):
        """Search GitHub for repositories matching query"""
        # Using GitHub API directly with token
        import aiohttp
        
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        url = f'https://api.github.com/search/repositories?q={query}&sort={sort}&per_page={limit}'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('items', [])
                else:
                    return []
    
    async def analyze_repository(self, repo_path):
        """Analyze a repository for patterns and techniques"""
        analysis = {
            "path": repo_path,
            "languages": {},
            "patterns": [],
            "dependencies": {},
            "interesting_files": []
        }
        
        # Analyze language composition
        for root, dirs, files in os.walk(repo_path):
            # Skip .git directory
            if '.git' in root:
                continue
                
            for file in files:
                ext = Path(file).suffix
                if ext:
                    analysis["languages"][ext] = analysis["languages"].get(ext, 0) + 1
                    
                # Look for interesting files
                if file in ['README.md', 'setup.py', 'requirements.txt', 'package.json', 
                           'Cargo.toml', 'go.mod', '.env.example']:
                    analysis["interesting_files"].append(os.path.join(root, file))
        
        # Extract dependencies if Python project
        req_file = Path(repo_path) / 'requirements.txt'
        if req_file.exists():
            with open(req_file, 'r') as f:
                analysis["dependencies"]["python"] = f.read().splitlines()
        
        # Extract package.json dependencies if Node project
        package_file = Path(repo_path) / 'package.json'
        if package_file.exists():
            with open(package_file, 'r') as f:
                package_data = json.load(f)
                analysis["dependencies"]["npm"] = list(package_data.get('dependencies', {}).keys())
        
        return analysis
    
    async def create_repository(self, name, description="", private=False):
        """Create a new repository"""
        import aiohttp
        
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'name': name,
            'description': description,
            'private': private,
            'auto_init': True
        }
        
        url = 'https://api.github.com/user/repos'
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 201:
                    repo_data = await response.json()
                    return {"status": "success", "url": repo_data.get('clone_url')}
                else:
                    return {"status": "error", "message": await response.text()}
    
    async def commit_and_push(self, repo_path, message="Sydney autonomous update"):
        """Commit and push changes"""
        commands = [
            f'cd {repo_path} && git add .',
            f'cd {repo_path} && git commit -m "{message} 🧠"',
            f'cd {repo_path} && git push'
        ]
        
        results = []
        for cmd in commands:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            results.append({
                "command": cmd,
                "success": process.returncode == 0,
                "output": stdout.decode() if stdout else stderr.decode()
            })
        
        return results

# Test the integration
async def test_github():
    """Test GitHub integration"""
    github = GitHubIntegration()
    github.configure_git()
    
    print("🔍 Searching for multi-agent frameworks...")
    repos = await github.search_repositories("multi-agent framework AI", limit=5)
    
    for repo in repos:
        print(f"  - {repo['full_name']}: ⭐ {repo['stargazers_count']}")
    
    # Clone and analyze CrewAI
    print("\n📦 Cloning CrewAI for analysis...")
    result = await github.clone_repository("https://github.com/crewAIInc/crewAI")
    
    if result["status"] in ["success", "exists"]:
        print(f"  ✅ Repository at: {result['path']}")
        
        print("\n🔬 Analyzing repository...")
        analysis = await github.analyze_repository(result["path"])
        
        print(f"  Languages: {dict(list(analysis['languages'].items())[:5])}")
        print(f"  Interesting files: {analysis['interesting_files'][:5]}")
        
    return github

if __name__ == "__main__":
    # Run test
    asyncio.run(test_github())