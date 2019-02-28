#!/bin/bash
sudo rm -r /home/ubuntu/html/
sudo mkdir /home/ubuntu/html
sudo chmod -R 777 /home/ubuntu/html
dos2unix /home/ubuntu/companieshousearchives.txt
input="/home/ubuntu/companieshousearchives.txt"
cd /home/ubuntu/html
while IFS= read -r var
do
  echo "$var"" start"
  wget "http://download.companieshouse.gov.uk/""$var"
  sudo unzip "$var" -d /home/ubuntu/html
  python3 /home/ubuntu/localscrap_my.py  
  echo "$var"" end"
done < "$input"
