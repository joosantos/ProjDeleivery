from core.utils import get_password_hash

"""
Command to execute script (must execute from project's root dir):
PYTHONPATH=. .venv/bin/python3 cli/get_pass_hash.py
"""


def main():
    print(get_password_hash("randomPass"))
    return


if __name__ == "__main__":
    main()
    print("END")
