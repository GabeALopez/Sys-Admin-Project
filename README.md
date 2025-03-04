# System Administration Project

This repo is for a System Administration class for Unix systems. This will contain code that will be used throughout the project for monitoring ubuntu servers.

## How to Install

### Setup

NOTE: This assumes that you are in the root sys-admin-project directory

**Linux:**

```bash
cd ..
mkdir venv
cd venv
python -m venv .
source ./bin/activate
cd ..
cd Sys-Admin-Project
pip install -r requirements.txt
```

**Windows:**

```bash
cd ..
mkdir venv
cd venv
python -m venv .
cmd
.\\Scripts\\activate
cd ..
cd Sys-Admin-Project
pip install -r requirements.txt
```

### Run locally

**Terminal one:**

```
python app.py
```

**Terminal two:**
```
python agent.py
```
