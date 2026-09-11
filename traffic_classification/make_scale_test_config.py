from pathlib import Path

output = Path(__file__).with_name("tenants.850-test.yaml")
with output.open("w", encoding="utf-8") as handle:
    for index in range(1, 851):
        handle.write(f"- name: scale-test-{index:04d}\n")
print(output)
