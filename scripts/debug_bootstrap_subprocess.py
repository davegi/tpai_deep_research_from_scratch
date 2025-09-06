import subprocess
import sys
import os
import tempfile
import textwrap

def main():
    tmpdir = tempfile.mkdtemp()
    env_path = os.path.join(tmpdir, ".env")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("MODEL_NAME=from-env\n")

    script = textwrap.dedent(f"""
import os
os.chdir({repr(tmpdir)})
import sys
sys.path.insert(0, {repr(os.path.abspath('src'))})
from research_agent_framework.bootstrap import bootstrap
bootstrap(force=True)
from research_agent_framework.config import get_settings
print(get_settings(force_reload=True).model_name)
""")

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmpdir,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": os.path.abspath("src"), "ENV_PATH": env_path},
    )

    print("returncode:", result.returncode)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

if __name__ == '__main__':
    main()
