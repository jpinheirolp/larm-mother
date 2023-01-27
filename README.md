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

## Explication du code 

Les deux fichiers launch exécutent plusieurs fichiers .py :

- scan_echo.py qui permet de renvoyer un nuage de points des alentours du robot. Ce nuage de points est créé à l’aide du laser du robot. Le nuage de point est envoyé dans un topic /scan

- move_randomly.py qui permet au robot de se déplacer de manière sûre dans son environnement.
Ce fichier récupère le nuage de points du topic /scan et adapte son mouvement en fonction de celui-ci. Plus précisément, il compte le nombre de points qu’il y a dans un rectangle délimité et très proche de lui. Si le nombre de point est supérieur à un certain nombre, celui-ci doit se stopper et tourner. Ce rectangle est divisé en deux ( rectangle droit et gauche ), et le robot compte alors le nombre de points à gauche et à droite. Si le nombre de point à gauche est plus important à droite, alors le robot tournera vers la gauche et inversement . Si le nombre de point dans son environnement proche est très petit, alors le robot va regarder dans un rectangle plus éloigné, et refait le même processus, à ceci près que le robot commencera à tourner tout en gardant une vitesse faible vers l’avant. Si le nombre de point est faible, alors il regarde dans un rectangle encore plus éloigné et la vitesse vers l’avant sera plus élevé. Enfin, si toujours rien, alors le robot peut se déplacer assez rapidement vers l’avant. 
Le gros problème à gérer fut celui de la gestion des obstacles dans lequel le nombre de points à gauche et à droite est quasiment le même (coin d’une pièce par exemple). Dans notre code initial, le robot rentrer dans une boucle infinie, tournant à gauche et à droite indéfiniment . Pour pallier à ce problème, nous disons au robot que si le nombre de point à gauche et à droite est le même à quelques points prêt, alors il droit tourner dans un même sens jusqu’à ce que ça ne soit pas le cas .
Enfin, afin que le robot puisse visiter l’ensemble d’une pièce, nous disons au robot qu’il doit tourner de manière aléatoire à une fréquence faible. 

- dans le cas du robot réel, le fichier launch minimal_launch .py est exécuté. Celui-ci permet d’avoir accés au laser ainsi qu’aux mouvements du robot.

- dans le cas de la simulation, c’est le fichier launch challenge-1.launch.py qui est exécuté, et qui est similaire au minimal_launch en plus de lancer une configuration de Gazebo .
Un remapping de la vélocité fut nécessaire afin de faire bouger le robot dans la simulation. 


# Challenge 2

L'objectif de ce challenge est de faire en sorte que le robot puisse faire une carte de la pièce dans laquelle le robot se déplace. Il sera de plus capable de repérer deux types de bouteilles :  Une bouteille orange et une bouteille noire Nuka-cola. A chaque fois que le robot détecte une bouteille, il affiche un message de détection, qui est pour notre code une image dans laquelle la bouteille est relevée dans l'image.

## Attention

Pour le moment, le robot n'est capable de détecter que les bouteilles oranges. La méthode de détection basée sur la couleur de la bouteille ne fonctionne pas avec les bouteilles noires, le noir n'étant pas une couleur.

## Comment exécuter la simulation du challenge-2

  - ouvrir le terminal 
  - copier et coller la commande ` ros2 launch pkg_mother challenge-2_sim.launch.py `
  
## Comment exécuter le challenge-2 sur le robot réel

  - ouvrir le terminal 
  - copier et coller la commande  ` ros2 launch pkg_mother challenge-2_robot.launch.py `

## Explication des algorithmes de detection testées

Première tentative : Notre première idée d'algorithme de vision afin de détecter la bouteille était très complexe. Nous avons mesuré la probabilité que la bouteille soit dans une image en calculant les distances dans un espace vectoriel défini. Dans cet espace vectoriel, chaque vecteur représente l'histogramme d'une image convertie en HSV. Une partie importante de l'algorithme était les centroïdes, les vecteurs qui représentent les histogrammes de couleurs les plus importantes dans le cadre de notre détection, l'orange de la bouteille, le noir de l'autre bouteille et le rouge du sol. Ils ont été créés en utilisant Kmeans avec k=1 dans un groupe d'images avec juste la couleur que nous voulions représenter. Après avoir eu le centroïde pour trouver si la bouteille est dans une image spécifique, nous divisons cette image en morceaux, puis nous calculons le vecteur de chacun des morceaux dans notre espace vectoriel d'histogramme de couleurs, et à la fin nous calculons la distance de ces vecteurs du morceaux au centroid. Si la distance est inférieure à une tolérance définie, nous disons que l'image contient la bouteille.
Cette méthode fut précise, cependant elle fut très lente, de l'ordre de 13 secondes pour le traitement d'une image, ce qui dans le cadre de notre robot en mouvement est inutile. Nous avons donc laissé tomber cette méthode. Cependant, les fonctions utilisées pour cette méthode est dans le fichier centroid_lib.py

Deuxième tentative : Étant donné que notre première tentative était trop lente, nous avons décidé d'essayer quelque chose de beaucoup plus simple et donc plus rapide. Dans cette deuxième méthode, nous commençons par convertir l'image en HSV, puis la filtrons de sorte qu'il ne reste comme couleurs qu'une plage qui ne contient que l'orange de la bouteille. Après cela, nous travaillons le masque qui vient du filtre. Nous subdivisons ce masque en plus petits morceaux et calculons simplement le nombre de pixels qu'il y a dans chaque morceau. Si le nombre de pixels est supérieur à la tolérance dans au moins un des morceaux on dit que l'image contient la bouteille orange.
En plus d'être très rapide, cette méthode est précise et les faux positifs sont très rare.

  
# Challenge 3

Le challenge 3 est dans la continuité du challenge 2. A l'issu de ce challenge, le robot doit être capable de mettre dans un repère un marqueur des bouteilles présentes dans l'arène, et de reconnaître une bouteille déjà relevée dans le repère. 

## Attention

Malheureusement, cette partie n'a pu être abordée par manque de temps. 



