from sympy import Rational

points = [(-1,9/20),(1,-11/20),(3/5,2),(-2,19/20),(-2,-4/3),(0,-2),(2,-21/20),(2,33/20),(-29/10,3),(-3,5/2),(-3,29/20),(-3,-1),(-3,-61/30),(-3,-3),(-1/10,-3),(3,-3),(3,-31/20),(3,7/5),(-4,101/30),(-4,5/2),(-4,39/20),(-4,-2/3),(-4,-17/10),(-4,-8/3),(-4,-29/10),(-4,-52/15),(-12/5,-4),(-7/10,-4),(0,-4),(29/10,-4),(4,-10/3),(4,-41/20),(4,23/20),(-5,37/10),(-5,5/2),(-5,49/20),(-5,-1/3),(-5,-41/30),(-5,-7/3),(-5,-77/30),(-5,-47/15),(-5,-23/5),(-19/5,-5),(3/5,-5),(23/10,-5),(3,-5),(5,-47/10),(5,-11/3),(5,-51/20),(5,9/10),(-6,121/30),(-6,14/5),(-6,0),(-6,-31/30),(-6,-2),(-6,-67/30),(-6,-14/5),(-6,-64/15),(-6,-79/15),(-19/5,-6),(-4/5,-6),(18/5,-6),(53/10,-6),(6,-6),(6,-151/30),(6,-4),(6,-61/20),(6,13/20),(-7,131/30),(-7,47/15),(-7,1/3),(-7,-7/10),(-7,-5/3),(-7,-19/10),(-7,-37/15),(-7,-59/15),(-7,-74/15),(-4/5,-7),(11/5,-7),(33/5,-7),(7,-197/30),(7,-19/3),(7,-161/30),(7,-13/3),(7,-71/20),(7,2/5),(-8,47/10),(-8,52/15),(-8,2/3),(-8,-11/30),(-8,-4/3),(-8,-47/30),(-8,-32/15),(-8,-18/5),(-8,-23/5),(11/5,-8),(26/5,-8),(8,-112/15),(8,-69/10),(8,-20/3),(8,-57/10),(8,-47/10),(8,-23/5),(8,-81/20),(8,3/20),(-9,151/30),(-9,19/5),(-9,1),(-9,-1/30),(-9,-1),(-9,-37/30),(-9,-9/5),(-9,-49/15),(-9,-64/15),(26/5,-9),(41/5,-9),(9,-39/5),(9,-217/30),(9,-7),(9,-181/30),(9,-26/5),(9,-23/5),(9,-91/20),(9,-1/10),(-10,161/30),(-10,62/15),(-10,4/3),(-10,3/10),(-10,-2/3),(-10,-9/10),(-10,-22/15),(-10,-44/15),(-10,-59/15),(41/5,-10),(10,-48/5),(10,-122/15),(10,-227/30),(10,-22/3),(10,-191/30),(10,-57/10),(10,-49/10),(10,-7/20),(-11,57/10),(-11,67/15),(-11,5/3),(-11,19/30),(-11,-1/3),(-11,-17/30),(-11,-17/15),(-11,-13/5),(-11,-18/5),(11,-164/15),(11,-149/15),(11,-127/15),(11,-79/10),(11,-23/3),(11,-67/10),(11,-31/5),(11,-157/30),(11,-3/5),(-12,181/30),(-12,24/5),(-12,2),(-12,29/30),(-12,0),(-12,-7/30),(-12,-4/5),(-12,-34/15),(-12,-49/15),(12,-169/15),(12,-154/15),(12,-44/5),(12,-247/30),(12,-8),(12,-211/30),(12,-67/10),(12,-167/30),(12,-17/20),(-13,191/30),(-13,77/15),(-13,7/3),(-13,13/10),(-13,1/3),(-13,1/10),(-13,-7/15),(-13,-29/15),(-13,-44/15),(13,-58/5),(13,-53/5),(13,-137/15),(13,-257/30),(13,-25/3),(13,-221/30),(13,-36/5),(13,-59/10),(13,-11/10),(-14,67/10),(-14,82/15),(-14,8/3),(-14,49/30),(-14,2/3),(-14,13/30),(-14,-2/15),(-14,-8/5),(-14,-13/5),(14,-179/15),(14,-164/15),(14,-142/15),(14,-89/10),(14,-26/3),(14,-77/10),(14,-187/30),(14,-27/20),(-15,211/30),(-15,29/5),(-15,3),(-15,59/30),(-15,1),(-15,23/30),(-15,1/5),(-15,-19/15),(-15,-34/15),(15,-184/15),(15,-169/15),(15,-49/5),(15,-277/30),(15,-9),(15,-163/20),(15,-121/15),(15,-197/30),(15,-8/5),(-16,221/30),(-16,92/15),(-16,10/3),(-16,23/10),(-16,4/3),(-16,11/10),(-16,8/15),(-16,-14/15),(-16,-29/15),(16,-63/5),(16,-58/5),(16,-152/15),(16,-287/30),(16,-187/20),(16,-93/10),(16,-173/20),(16,-42/5),(16,-73/10),(16,-67/10),(16,-37/20),(-17,77/10),(-17,97/15),(-17,11/3),(-17,79/30),(-17,5/3),(-17,43/30),(-17,13/15),(-17,-3/5),(-17,-8/5),(17,-194/15),(17,-179/15),(17,-157/15),(17,-10),(17,-49/5),(17,-93/10),(17,-183/20),(17,-44/5),(17,-43/5),(17,-83/10),(17,-67/10),(17,-21/10),(-18,241/30),(-18,34/5),(-18,4),(-18,89/30),(-18,2),(-18,53/30),(-18,6/5),(-18,-4/15),(-18,-19/15),(18,-199/15),(18,-184/15),(18,-54/5),(18,-21/2),(18,-152/15),(18,-143/15),(18,-93/10),(18,-43/5),(18,-67/10),(18,-47/20),(-19,251/30),(-19,107/15),(-19,13/3),(-19,33/10),(-19,7/3),(-19,21/10),(-19,23/15),(-19,1/15),(-19,-14/15),(19,-68/5),(19,-63/5),(19,-113/10),(19,-164/15),(19,-211/20),(19,-246/25),(19,-43/5),(19,-67/10),(19,-13/5),(-20,87/10),(-20,112/15),(-20,14/3),(-20,109/30),(-20,8/3),(-20,73/30),(-20,28/15),(-20,2/5),(-20,-3/5),(20,-209/15),(20,-194/15),(20,-59/5),(20,-347/30),(20,-219/20),(20,-251/25),(20,-43/5),(20,-67/10),(20,-57/20),(-21,271/30),(-21,39/5),(-21,5),(-21,119/30),(-21,3),(-21,83/30),(-21,11/5),(-21,11/15),(-21,-4/15),(21,-214/15),(21,-199/15),(21,-127/10),(21,-243/20),(21,-229/20),(21,-256/25),(21,-43/5),(21,-67/10),(21,-31/10),(-22,281/30),(-22,122/15),(-22,16/3),(-22,43/10),(-22,10/3),(-22,31/10),(-22,38/15),(-22,16/15),(-22,1/15),(22,-73/5),(22,-55/4),(22,-27/2),(22,-253/20),(22,-239/20),(22,-261/25),(22,-43/5),(22,-67/10),(22,-67/20),(-23,97/10),(-23,127/15),(-23,17/3),(-23,139/30),(-23,11/3),(-23,103/30),(-23,43/15),(-23,7/5),(-23,2/5),(23,-299/20),(23,-149/10),(23,-57/4),(23,-14),(23,-263/20),(23,-249/20),(23,-109/10),(23,-157/15),(23,-43/5),(23,-67/10),(23,-18/5),(-24,301/30),(-24,44/5),(-24,6),(-24,149/30),(-24,4),(-24,113/30),(-24,16/5),(-24,26/15),(-24,11/15),(24,-309/20),(24,-59/4),(24,-29/2),(24,-273/20),(24,-13),(24,-64/5),(24,-119/10),(24,-109/10),(24,-157/15),(24,-43/5),(24,-67/10),(24,-77/20),(-25,311/30),(-25,137/15),(-25,19/3),(-25,53/10),(-25,13/3),(-25,41/10),(-25,53/15),(-25,31/15),(-25,16/15),(25,-319/20),(25,-153/10),(25,-224/15),(25,-283/20),(25,-41/3),(25,-257/20),(25,-109/10),(25,-157/15),(25,-43/5),(25,-67/10),(25,-41/10),(-26,107/10),(-26,142/15),(-26,20/3),(-26,169/30),(-26,14/3),(-26,133/30),(-26,58/15),(-26,12/5),(-26,7/5),(26,-329/20),(26,-79/5),(26,-229/15),(26,-293/20),(26,-72/5),(26,-143/10),(26,-267/20),(26,-109/10),(26,-157/15),(26,-43/5),(26,-67/10),(26,-87/20),(-27,331/30),(-27,49/5),(-27,7),(-27,179/30),(-27,5),(-27,143/30),(-27,21/5),(-27,41/15),(-27,26/15),(27,-339/20),(27,-82/5),(27,-81/5),(27,-303/20),(27,-449/30),(27,-74/5),(27,-71/5),(27,-27/2),(27,-109/10),(27,-157/15),(27,-43/5),(27,-67/10),(27,-23/5),(-28,341/30),(-28,152/15),(-28,22/3),(-28,63/10),(-28,16/3),(-28,51/10),(-28,68/15),(-28,46/15),(-28,31/15),(28,-349/20),(28,-87/5),(28,-167/10),(28,-79/5),(28,-77/5),(28,-613/40),(28,-76/5),(28,-27/2),(28,-109/10),(28,-157/15),(28,-43/5),(28,-67/10),(28,-97/20),(-29,117/10),(-29,157/15),(-29,23/3),(-29,199/30),(-29,17/3),(-29,163/30),(-29,73/15),(-29,17/5),(-29,12/5),(29,-181/10),(29,-521/30),(29,-163/10),(29,-633/40),(29,-63/4),(29,-153/10),(29,-27/2),(29,-109/10),(29,-157/15),(29,-43/5),(29,-67/10),(29,-51/10),(-30,361/30),(-30,54/5),(-30,8),(-30,209/30),(-30,6),(-30,173/30),(-30,26/5),(-30,56/15),(-30,41/15),(30,-563/30),(30,-541/30),(30,-84/5),(30,-653/40),(30,-65/4),(30,-153/10),(30,-27/2),(30,-109/10),(30,-157/15),(30,-43/5),(30,-67/10),(30,-107/20),(-31,371/30),(-31,167/15),(-31,25/3),(-31,73/10),(-31,19/3),(-31,61/10),(-31,83/15),(-31,61/15),(-31,46/15),(31,-583/30),(31,-187/10),(31,-173/10),(31,-673/40),(31,-67/4),(31,-153/10),(31,-27/2),(31,-109/10),(31,-157/15),(31,-43/5),(31,-67/10),(31,-28/5),(-32,127/10),(-32,172/15),(-32,26/3),(-32,229/30),(-32,20/3),(-32,193/30),(-32,88/15),(-32,22/5),(-32,17/5),(32,-201/10),(32,-581/30),(32,-89/5),(32,-693/40),(32,-69/4),(32,-153/10),(32,-27/2),(32,-109/10),(32,-157/15),(32,-43/5),(32,-67/10),(32,-117/20),(-33,391/30),(-33,59/5),(-33,9),(-33,239/30),(-33,7),(-33,203/30),(-33,31/5),(-33,71/15),(-33,56/15),(33,-623/30),(33,-601/30),(33,-183/10),(33,-713/40),(33,-71/4),(33,-153/10),(33,-27/2),(33,-109/10),(33,-157/15),(33,-43/5),(33,-67/10),(33,-61/10),(-34,401/30),(-34,182/15),(-34,28/3),(-34,83/10),(-34,22/3),(-34,71/10),(-34,98/15),(-34,76/15),(-34,61/15),(34,-643/30),(34,-207/10),(34,-94/5),(34,-733/40),(34,-73/4),(34,-153/10),(34,-27/2),(34,-109/10),(34,-157/15),(34,-67/10),(34,-127/20),(-35,137/10),(-35,187/15),(-35,29/3),(-35,259/30),(-35,23/3),(-35,223/30),(-35,103/15),(-35,27/5),(-35,22/5),(35,-221/10),(35,-641/30),(35,-193/10),(35,-753/40),(35,-75/4),(35,-153/10),(35,-27/2),(35,-109/10),(35,-157/15),(35,-43/5),(35,-67/10),(35,-33/5),(-36,421/30),(-36,64/5),(-36,10),(-36,269/30),(-36,8),(-36,233/30),(-36,36/5),(-36,86/15),(-36,71/15),(36,-683/30),(36,-661/30),(36,-99/5),(36,-773/40),(36,-77/4),(36,-153/10),(36,-27/2),(36,-109/10),(36,-157/15),(36,-43/5),(36,-34/5),(-37,431/30),(-37,197/15),(-37,31/3),(-37,93/10),(-37,25/3),(-37,81/10),(-37,113/15),(-37,91/15),(-37,76/15),(37,-703/30),(37,-227/10),(37,-203/10),(37,-793/40),(37,-79/4),(37,-153/10),(37,-27/2),(37,-109/10),(37,-157/15),(37,-43/5),(37,-209/30),(-38,147/10),(-38,202/15),(-38,32/3),(-38,289/30),(-38,26/3),(-38,253/30),(-38,118/15),(-38,32/5),(-38,27/5),(38,-241/10),(38,-701/30),(38,-104/5),(38,-813/40),(38,-81/4),(38,-153/10),(38,-27/2),(38,-109/10),(38,-157/15),(38,-43/5),(38,-107/15),(-39,451/30),(-39,69/5),(-39,11),(-39,299/30),(-39,9),(-39,263/30),(-39,41/5),(-39,101/15),(-39,86/15),(39,-743/30),(39,-721/30),(39,-213/10),(39,-833/40),(39,-83/4),(39,-153/10),(39,-27/2),(39,-109/10),(39,-157/15),(39,-43/5),(39,-73/10),(-40,461/30),(-40,212/15),(-40,34/3),(-40,103/10),(-40,28/3),(-40,91/10),(-40,128/15),(-40,106/15),(-40,91/15),(40,-763/30),(40,-247/10),(40,-109/5),(40,-853/40),(40,-85/4),(40,-153/10),(40,-27/2),(40,-109/10),(40,-157/15),(40,-43/5),(40,-112/15),(-41,157/10),(-41,217/15),(-41,35/3),(-41,319/30),(-41,29/3),(-41,283/30),(-41,133/15),(-41,37/5),(-41,32/5),(41,-261/10),(41,-761/30),(41,-223/10),(41,-873/40),(41,-87/4),(41,-153/10),(41,-27/2),(41,-109/10),(41,-157/15),(41,-43/5),(41,-229/30),(-42,481/30),(-42,74/5),(-42,12),(-42,329/30),(-42,10),(-42,293/30),(-42,46/5),(-42,116/15),(-42,101/15),(42,-803/30),(42,-781/30),(42,-114/5),(42,-893/40),(42,-89/4),(42,-153/10),(42,-27/2),(42,-109/10),(42,-157/15),(42,-43/5),(42,-39/5),(-43,491/30),(-43,227/15),(-43,37/3),(-43,113/10),(-43,31/3),(-43,101/10),(-43,143/15),(-43,121/15),(-43,106/15),(43,-823/30),(43,-267/10),(43,-233/10),(43,-913/40),(43,-91/4),(43,-153/10),(43,-27/2),(43,-109/10),(43,-157/15),(43,-43/5),(43,-239/30),(-44,167/10),(-44,232/15),(-44,38/3),(-44,349/30),(-44,32/3),(-44,313/30),(-44,148/15),(-44,42/5),(-44,37/5),(44,-281/10),(44,-821/30),(44,-119/5),(44,-933/40),(44,-93/4),(44,-153/10),(44,-27/2),(44,-109/10),(44,-157/15),(44,-43/5),(44,-122/15),(-45,511/30),(-45,79/5),(-45,13),(-45,359/30),(-45,11),(-45,323/30),(-45,51/5),(-45,131/15),(-45,116/15),(45,-863/30),(45,-841/30),(45,-243/10),(45,-953/40),(45,-95/4),(45,-153/10),(45,-27/2),(45,-109/10),(45,-157/15),(45,-43/5),(45,-83/10),(-46,521/30),(-46,242/15),(-46,40/3),(-46,123/10),(-46,34/3),(-46,111/10),(-46,158/15),(-46,136/15),(-46,121/15),(46,-883/30),(46,-287/10),(46,-124/5),(46,-973/40),(46,-97/4),(46,-153/10),(46,-27/2),(46,-109/10),(46,-157/15),(46,-43/5),(46,-127/15),(-47,177/10),(-47,247/15),(-47,41/3),(-47,379/30),(-47,35/3),(-47,343/30),(-47,163/15),(-47,47/5),(-47,42/5),(47,-301/10),(47,-881/30),(47,-253/10),(47,-993/40),(47,-99/4),(47,-153/10),(47,-27/2),(47,-109/10),(47,-157/15),(47,-302/35),(-48,541/30),(-48,84/5),(-48,14),(-48,389/30),(-48,12),(-48,353/30),(-48,56/5),(-48,146/15),(-48,131/15),(48,-923/30),(48,-901/30),(48,-129/5),(48,-1013/40),(48,-101/4),(48,-153/10),(48,-27/2),(48,-109/10),(48,-157/15),(48,-307/35),(-49,551/30),(-49,257/15),(-49,43/3),(-49,133/10),(-49,37/3),(-49,121/10),(-49,173/15),(-49,151/15),(-49,136/15),(49,-943/30),(49,-307/10),(49,-263/10),(49,-1033/40),(49,-103/4),(49,-153/10),(49,-27/2),(49,-109/10),(49,-157/15),(49,-312/35)]

newPoints = []
for a, c in points:
    newPoints.append(((a) + (3*c), (c)))


print(*newPoints, sep=",")