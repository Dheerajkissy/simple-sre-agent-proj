import sys

def analyze_log(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    errors = [line for line in lines if 'ERROR' in line]
    warnings = [line for line in lines if 'WARNING' in line]

    print("🔍 Log Summary:")
    print(f"  Errors: {len(errors)}")
    for e in errors:
        print(f"    - {e.strip()}")

    print(f"  Warnings: {len(warnings)}")
    for w in warnings:
        print(f"    - {w.strip()}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sre_agent.py <log_file>")
    else:
        analyze_log(sys.argv[1])

