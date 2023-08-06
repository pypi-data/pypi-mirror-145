import json
import sys


def get_param(paramname):
    fa = json.loads(sys.argv[1])
    try:
        return fa[paramname]
    except Exception as e:
        print(f"Parameter {paramname} not found!")


def get_secret(secretname):
    fa = json.loads(sys.argv[1])
    try:
        return fa['secrets'][secretname]
    except Exception as e:
        print(f"Secret {secretname} not found!")


