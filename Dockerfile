

[4/8] RUN python -m venv /app/venv  ✔ 3s

[5/8] RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

Requirement already satisfied: pip in ./venv/lib/python3.10/site-packages (23.0.1)

Collecting pip

  Downloading pip-25.0.1-py3-none-any.whl (1.8 MB)

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 39.0 MB/s eta 0:00:00



Requirement already satisfied: setuptools in ./venv/lib/python3.10/site-packages (65.5.0)

Collecting setuptools

  Downloading setuptools-76.0.0-py3-none-any.whl (1.2 MB)

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 152.7 MB/s eta 0:00:00



Collecting wheel

  Downloading wheel-0.45.1-py3-none-any.whl (72 kB)

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72.5/72.5 kB 30.5 MB/s eta 0:00:00



Installing collected packages: wheel, setuptools, pip

  Attempting uninstall: setuptools

    Found existing installation: setuptools 65.5.0

    Uninstalling setuptools-65.5.0:

      Successfully uninstalled setuptools-65.5.0

  Attempting uninstall: pip

    Found existing installation: pip 23.0.1

    Uninstalling pip-23.0.1:

      Successfully uninstalled pip-23.0.1

Successfully installed pip-25.0.1 setuptools-76.0.0 wheel-0.45.1

[5/8] RUN /app/venv/bin/pip install --upgrade pip setuptools wheel  ✔ 2s

[6/8] COPY requirements.txt .

[6/8] COPY requirements.txt .  ✔ 19ms

[7/8] RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

Collecting git+https://github.com/Discord-Voice/ext-voice.git@main (from -r requirements.txt (line 2))

  Cloning https://github.com/Discord-Voice/ext-voice.git (to revision main) to /tmp/pip-req-build-bon2t3wt

  Running command git clone --filter=blob:none --quiet https://github.com/Discord-Voice/ext-voice.git /tmp/pip-req-build-bon2t3wt

  fatal: could not read Username for 'https://github.com';: No such device or address

  error: subprocess-exited-with-error
  
  × git clone --filter=blob:none --quiet https://github.com/Discord-Voice/ext-voice.git /tmp/pip-req-build-bon2t3wt did not run successfully.
  │ exit code: 128
  ╰─> See above for output.
  
  note: This error originates from a subprocess, and is likely not a problem with pip.

error: subprocess-exited-with-error

× git clone --filter=blob:none --quiet https://github.com/Discord-Voice/ext-voice.git /tmp/pip-req-build-bon2t3wt did not run successfully.
│ exit code: 128
╰─> See above for output.

note: This error originates from a subprocess, and is likely not a problem with pip.

✕ [7/8] RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt 
process "/bin/sh -c /app/venv/bin/pip install --no-cache-dir -r requirements.txt" did not complete successfully: exit code: 1
 
