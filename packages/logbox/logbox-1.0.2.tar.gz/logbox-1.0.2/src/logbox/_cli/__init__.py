# Copyright (C) 2021 Matthias Nadig

import sys

if sys.platform == 'win32':
    from ._windows import activate_esc, deactivate_esc
else:
    from ._bypass import bypass as activate_esc
    from ._bypass import bypass as deactivate_esc
