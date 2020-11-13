'''
titan2 - Gemini Protocol Client Transport Library
Copyright (C) 2020  Chris Brousseau

titan2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

titan2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with titan2.  If not, see <https://www.gnu.org/licenses/>.
'''

import sys

# Polyfill to include gemini in urllib parsing
if sys.version_info > (3, 10):
  raise Exception("Python versions > 3.9.x are not supported at this time.")
elif sys.version_info > (3, 9):
  from .python3_9.Lib import urllib
elif sys.version_info > (3, 8):
  from .python3_8.Lib import urllib
elif sys.version_info > (3, 7):
  from .python3_7.Lib import urllib
else:
  raise Exception("Python versions < 3.7 are not supported at this time.")