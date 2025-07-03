#!/usr/bin/env python3
"""
Test rapide pour voir quelle méthode de lecture HDFS fonctionne le mieux
"""
import subprocess
import requests
import time

def test_api_rest():
    """Test API REST WebHDFS"""
    try:
        print("🔬 Test API REST WebHDFS...")
        response = requests.get("http://localhost:9870/webhdfs/v1/music_events/year=2025/month=07/day=03/batch_20250703_164506.jsonl?op=OPEN", 
                              timeout=10, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content length: {len(response.text)}")
        if response.text:
            print(f"First 200 chars: {response.text[:200]}")
        return len(response.text) > 0
    except Exception as e:
        print(f"❌ API REST failed: {e}")
        return False

def test_docker_cli():
    """Test Docker CLI"""
    try:
        print("\n🔬 Test Docker CLI...")
        start = time.time()
        cmd = ["docker", "exec", "namenode", "hdfs", "dfs", "-cat", "/music_events/year=2025/month=07/day=03/batch_20250703_164506.jsonl"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        elapsed = time.time() - start
        
        print(f"Return code: {result.returncode}")
        print(f"Elapsed: {elapsed:.2f}s")
        print(f"Stdout length: {len(result.stdout)}")
        print(f"Stderr: {result.stderr}")
        
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            print(f"Lines: {len(lines)}")
            print(f"First line: {lines[0] if lines else 'None'}")
            
        return result.returncode == 0 and len(result.stdout) > 0
    except Exception as e:
        print(f"❌ Docker CLI failed: {e}")
        return False

if __name__ == '__main__':
    api_works = test_api_rest()
    cli_works = test_docker_cli()
    
    print(f"\n📊 Résultats:")
    print(f"API REST: {'✅' if api_works else '❌'}")
    print(f"Docker CLI: {'✅' if cli_works else '❌'}")
