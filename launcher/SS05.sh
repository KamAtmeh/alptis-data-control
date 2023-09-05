echo "Lancement des contrôles de fichiers de SS05"
echo "Création des dossiers temporaires"

FILE_TO_WATCH=/tmp/log/CS_SS05.log
FILE_CC=/tmp/log/CC_SS05.log
PATTERN='Retrieve\sinput\sCSV\sfiles\sfrom'

cd /tmp/
mkdir input/
mkdir input/SS05/
mkdir output/
mkdir log

cp -r /data/migration/contrat/SS05/F* input/SS05

cd /var/controle-migration/
python -m robot --output None --log None --report None --variable PROD_NAME:"SS05" robot-tests/test/controle_simple.robot > ${FILE_TO_WATCH} &

i=0
while [ ${i} -lt 200 ]; do
	((i++)); sleep 5
	if grep -E ${PATTERN} ${FILE_TO_WATCH}; then
		break
	fi
done

echo "Lancement des controles complexes"
python -m robot --output None --log None --report None --variable PROD_NAME:"SS05" robot-tests/test/controle_complexe.robot > ${FILE_CC}

cd /tmp/
cp -r output/* /data/migration/contrat/OUTPUT/robot/

rm -r input
rm -r output

cd ~

