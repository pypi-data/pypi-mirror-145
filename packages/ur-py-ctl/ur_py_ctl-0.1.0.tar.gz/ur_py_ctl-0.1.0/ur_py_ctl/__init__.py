import pathlib

__version__ = "0.1.0"

HERE = pathlib.Path(__file__).parent
REPO_DIR = HERE.parent
DATA_DIR = REPO_DIR / "data"
LOG_DIR = REPO_DIR / "log"

from .urscript_commands import Motion  # noqa: F401,E402
from .urscript_commands import move_to_pose  # noqa: F401,E402
from .urscript_commands import move_to_conf  # noqa: F401,E402
from .urscript_commands import set_tcp  # noqa: F401,E402
from .urscript_commands import set_DO  # noqa: F401,E402
from .urscript_commands import read_DO  # noqa: F401,E402
from .urscript_commands import set_AO  # noqa: F401,E402
from .urscript_commands import read_AO  # noqa: F401,E402
from .urscript_commands import sleep  # noqa: F401,E402
from .urscript_commands import text_msg  # noqa: F401,E402
from .urscript_commands import popup  # noqa: F401,E402
