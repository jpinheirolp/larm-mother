# UV LARM Groupe 7 Mother

Ce git est issu d'un projet de cours de Logiciels et applications pour la robotique mobile à l'IMT NORD EUROPE. 
# Le repertoire LARM_MOTHER

Le repertoire Larm_mother permet de au robot Kobuki de se déplacer dans une pièce. Grâce aux différents fichiers, vous pourrez executer un déplacement autonome du robot, scaner d'une pièce, établir une carte d'une pièce et reconnaître divers objets dans son environnement. 
Vous serez également en capacité de visualiser ce que le robot observe gràce à Rviz2, et d'observer des simulations de robot grâce à Gazebo. 

- L'ensemble des scripts sont écrits en Python: https://www.python.org/
- Le robot fonctionne sous ROS2: https://docs.ros.org/en/foxy/Tutorials/Intermediate/Launch/Launch-Main.html

## Comment installer le repertoire

- Installer ros2 et Python 3 
- Créer un workspace (repertoire)
- Ouvrir le shell
- Rentrer dans votre workspace
- cloner et installer tbot `https://bitbucket.org/imt-mobisyst/mb6-tbot` 
- insérer la commande `git clone https://github.com/jpinheirolp/larm-mother.git`

## Attention 

Il est bon à noter qu'avant de lancer chaque commande ROS, il faut revenir dans votre répertoire ros2 et lancer la commande ` colcon build ` dans votre shell, puis `source install/setup.bash `

# Challenge 1

L'objectif de ce challenge 1 est de faire en sorte que le robot puisse se déplacer dans un espace contenant des obstacles sans avoir de collision. 
Pour cela nous avons 3 fichier launch:
- Un fichier challenge-1_sim.launch.py qui permet d'éxécuter une simulation du challenge 1 via Gazebo
- Un fichier challenge-1_robot.launch.py qui permet d'éxécuter le challenge 1 sur le robot réel 
- Un fichier challenge-1_visualize.launch.py qui permet d'observer le nuage de points réalisé par le laser du robot via RVIZ2

## Comment exécuter la simulation du challenge-1

  - ouvrir le terminal
  - copier et coller la commande ` ros2 launch pkg_mother challenge-1_sim.launch.py `

## Comment exécuter le challenge-1 sur le robot réel

  - ouvrir le terminal 
  - copier et coller la commande  ` ros2 launch pkg_mother challenge-1_robot.launch.py `
  
## Comment exécuter la visualisation

  - ouvrir le terminal 
  - copier et coller la commande ` ros2 launch pkg_mother challenge-1_visualize.launch.py `

# Challenge 2

L'objectif de ce challenge est de faire en sorte que le robot puisse faire une carte de la pièce dans laquelle le robot se déplace. Il sera de plus capable de repérer deux types de bouteilles :  Une bouteille orange et une bouteille noire Nuka-cola. A chaque fois que le robot détecte une bouteille, il affiche un message de détection, qui est pour notre code une image dans laquelle la bouteille est relevée dans l'image.

## Attention

Pour le moment, le robot n'est capable de détecter que les bouteilles orange. La méthode basée de détection basée sur la couleur de la bouteille ne fonctionne pas avec les bouteilles noires, le noir n'étant pas une couleur.

## Comment exécuter la simulation du challenge-2

  - ouvrir le terminal 
  - copier et coller la commande ` ros2 launch pkg_mother challenge-2_sim.launch.py `
  
 ## Comment exécuter le challenge-2 sur le robot réel

  - ouvrir le terminal 
  - copier et coller la commande  ` ros2 launch pkg_mother challenge-2_robot.launch.py `
  
# Challenge 3

Le challenge 3 est dans la continuité du challenge 2. A l'issu de ce challenge, le robot doit être capable de mettre dans un repère un marqueur des bouteilles présentes dans l'arène, et de reconnaître une bouteille déjà relevée dans le repère. 

## Attention

Malheureusement, cette partie n'a pu être abordée par manque de temps. 
