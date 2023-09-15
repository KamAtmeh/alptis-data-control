(echo "Simple"; python -m robot robot-tests/test/controle_simple.robot) &
	(echo "Complexe"; python -m robot robot-tests/test/controle_complexe.robot)
wait
