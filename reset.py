#!/usr/bin/env python3
import subprocess
import sys

def run(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    try:
        if "--down" in sys.argv:
            run(["docker", "compose", "down", "-v"])
        else:
            run(["docker", "compose", "down", "-v"])
            run(["docker", "compose", "up", "-d", "--build"])
            print("\nEnvironment is up! Wait for healthchecks to pass.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
