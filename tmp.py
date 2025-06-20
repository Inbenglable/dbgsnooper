# debug_requirements.py
from setuptools import setup
print("=== DEBUG ===")

REQUIREMENTS = []

with open('requirements.in') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            REQUIREMENTS.append(line)

print("install_requires =", REQUIREMENTS)

setup(
    name='dbgsnooper',
    version='0.0.1',
    install_requires=REQUIREMENTS,
)
