# Execution commands

1. create environment:

```bash
poetry install
```

2. start server:

```bash
poetry run python server.py
```

3. make requests to the server:

```bash
curl -X POST "http://localhost:8000/agent" \
     -H "Content-Type: application/json" \
     -d '{"msg": "I want to find all files in directory `~/AnotherAgent/test_directory` with `.txt` extension. Then for those of these files which contain at least 1 word `log` inside their filename, change their extension to `.log`"}'
```
