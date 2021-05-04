# Functions below taken from the Python package deterministic zip:

# Copyright (c) 2019, Bryce Boe
# Copyright (c) 2019, AppFolio, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import zipfile
import stat

def add_directory(zip_file, path, zip_path):
    print(zip_file)
    print(path)
    print(zip_path)
    for item in sorted(os.listdir(path)):
        current_path = os.path.join(path, item)
        current_zip_path = os.path.join(zip_path, item)
        if os.path.isfile(current_path):
            add_file(zip_file, current_path, current_zip_path)
        else:
            add_directory(zip_file, current_path, current_zip_path)
            
            
def add_file(zip_file, path, zip_path=None):
    permission = 0o555 if os.access(path, os.X_OK) else 0o444
    zip_info = zipfile.ZipInfo.from_file(path, zip_path)
    zip_info.date_time = (2021, 1, 1, 1, 1, 1)
    zip_info.external_attr = (stat.S_IFREG | permission) << 16
    with open(path, "rb") as fp:
        zip_file.writestr(
            zip_info,
            fp.read(),
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        )

