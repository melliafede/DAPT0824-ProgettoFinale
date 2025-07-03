import os
import re

directory = "tennis_atp-master"
file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

pattern = re.compile(r'^atp_matches_\d{4}\.csv$')
files = [f for f in file_names if pattern.match(f)]
print(files)