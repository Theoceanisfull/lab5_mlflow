#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# Airflow setup script (pinned to Python 3.11)
# ------------------------------------------------------------

AIRFLOW_VERSION="2.10.2"
PYTHON_BIN="python3.11"  # force Python 3.11 interpreter

# Verify Python 3.11 is installed
if ! command -v ${PYTHON_BIN} &>/dev/null; then
  echo "❌ ${PYTHON_BIN} not found. Please install Python 3.11 first."
  echo "On macOS: brew install python@3.11"
  exit 1
fi

# Detect Python version (should be 3.11)
PY_VER=$(${PYTHON_BIN} -c 'import sys;print(f"{sys.version_info[0]}.{sys.version_info[1]}")')

# Airflow constraints URL for matching Python version
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PY_VER}.txt"

# ------------------------------------------------------------
# Create and activate virtual environment (Python 3.11)
# ------------------------------------------------------------
${PYTHON_BIN} -m venv .venv
source .venv/bin/activate

# Upgrade packaging tools
pip install --upgrade pip wheel setuptools

# ------------------------------------------------------------
# Install Airflow + project dependencies
# ------------------------------------------------------------
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install -r requirements.txt

echo "✅ Setup complete."
echo "Virtual environment: $(python --version)"
echo "Airflow version: $(airflow version)"
