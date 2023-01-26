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
Pour cela nous avons 3 fichiers launch:
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


## Visualisation

Première tentative : Notre première idée de créer un algorithme de vision par ordinateur pour trouver la bouteille était très complexe. Nous avons mesuré la probabilité que la bouteille soit dans une image en calculant les distances dans un espace vectoriel défini. Dans cet espace vectoriel, chaque vecteur représente l'histogramme d'une image convertie en HSV. Une partie importante de l'algorithme était les centroïdes, les vecteurs qui représentent les histogrammes de couleurs les plus importants, l'orange de la bouteille, le noir de l'autre bouteille et le rouge du sol. Ils ont été créés en utilisant Kmeans avec k=1 dans un groupe d'images avec juste la couleur que nous voulions représenter. Après avoir eu le centroïde pour trouver si la bouteille est dans une image spécifique, nous divisons cette image en morceaux, puis nous calculons le vecteur de cette morceaux dans notre espace vectoriel d'histogramme de couleurs, et à la fin nous calculons la distance de ces vecteurs du pièces au centroid. Si la distance est inférieure à une tolérance définie, nous disons que l'image contient la bouteille.

Deuxième tentative : puisque notre première tentative était de ralentir, nous avons décidé d'essayer quelque chose de beaucoup plus simple qui pourrait être beaucoup plus rapide. Dans cette deuxième méthode, nous commençons par convertir l'image en HSV, puis la filtrons vers une plage qui ne contient que l'orange de la bouteille. Après cela, nous travaillons le masque qui vient du filtre. Nous subdivisons ce masque en plus petits morceaux et simplement le nombre de pixels qu'il y a dans chaque morceau. Si le nombre de pixels est supérieur à la tolérance dans au moins un des morceaux on dit que l'image contient la bouteille orange.
