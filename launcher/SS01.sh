echo "Lancement des contrôles de fichiers de SS01"
echo "Création des dossiers temporaires"

cd /tmp/

mkdir input/
mkdir input/SS01/
mkdir output/

cp -r /data/migration/contrat/LSC/F* input/SS01/

cd /var/controle-migration/
python -m robot --report None --log None --output None --variable PROD_NAME:"SS01" robot-tests/test/controle_simple.robot
python -m robot --report None --log None --output None --variable PROD_NAME:"SS01" robot-tests/test/controle_complexe.robot

cd /tmp/
cp -r output/* /data/migration/contrat/OUTPUT/robot/

rm -r input
rm -r output

cd ~
