import subprocess
import pandas as pd
df = pd.read_csv(r'manesht_new/url_list.csv')
df = df[['Link']]
df.to_csv("sites.txt", header=False, index=False)


url = "sites.txt" 
command = ["gospider","-S", url,"-o","output","-c",str(10),"-d",str(1),"--blacklist",".(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico)" ]
process = subprocess.run(command, capture_output=True)

if process.returncode == 0:
    print(process.stdout.decode("utf-8"))
else:
    print(f"Error: {process.stderr.decode('utf-8')}")
    
