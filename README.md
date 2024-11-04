# Execution commands

1. create environment:

```bash
poetry install
```

2. start server:

```bash
poetry run python server.py
```

3. create a test directory that contains the files to be tested.

```
mkdir test_directory
touch a.txt
touch b.txt
touch c.txt
touch d_log.txt
```

4. make requests to the server:

```bash
curl -X POST "http://localhost:8000/agent" \
     -H "Content-Type: application/json" \
     -d '{"msg": "I want to find all files in directory `test_directory` with `.txt` extension. Then for those of these files which contain at least 1 word `log` inside their filename, change their extension to `.log`"}'
```

# Notice

The code is only focusing on functionality. The Google AI sometimes would not be able to successfully finish the requirements. But the pipeline of accepting requirements and finishing commands is functional.
