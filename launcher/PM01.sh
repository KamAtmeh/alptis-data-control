echo "Lancement des contrôles de fichiers de PM01"
echo "Création des dossiers temporaires"

cd /tmp/
mkdir input/
mkdir input/PM01/
mkdir output

cp -r /data/migration/contrat/PM01/F* input/PM01/

cd /var/controle-migration/
python -m robot --report None --log None --output None --variable PROD_NAME:"PM01" robot-tests/test/controle_simple.robot
python -m robot --report None --log None --output None --variable PROD_NAME:"PM01" robot-tests/test/controle_complexe.robot

cd /tmp/
cp -r output/* /data/migration/contrat/OUTPUT/robot/

rm -r input
rm -r output

cd ~
