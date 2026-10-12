# Résultats — sept tables logistiques

Ces statistiques proviennent de l'exécution des quatre notebooks sur les **sept** fichiers ERP fournis.

## Cours 1 — Nettoyage, intégrité et statistiques

| Table | Lignes initiales | Après suppression des doublons exacts |
|---|---:|---:|
| Partenaires | 80 | 80 |
| Sites | 30 | 30 |
| Commandes d'achat (lignes) | 651 | 650 |
| Réceptions | 612 | 610 |
| Expéditions | 452 | 450 |
| Ajustements | 140 | 140 |
| Inventaires mensuels | 502 | 500 |

**7 doublons exacts** supprimés, sans supprimer les transactions présentant seulement le même fournisseur. **14 partenaires** sans numéro d'immatriculation externe renseigné. Pour toutes les réceptions nettoyées, la clé composite de commande existe : **0 réception sans ligne PO**. Les clés de partenaire et de site utilisées dans les expéditions existent aussi dans le référentiel ERP.

## Cours 2 — Similarité et clustering

Deux représentations séparées : **80 profils partenaires** enrichis par leurs nombres de lignes de commande et d'expédition (envoyées/reçues/transportées), et **30 profils de sites** enrichis par départs/arrivées, commandes, réceptions, ajustements et inventaires. K-means a retenu **5 groupes** de partenaires et **2 groupes** de sites, parmi les nombres de clusters testés, selon la silhouette.

## Cours 3 — Associations et cohérences inter-tables

- Les règles Apriori portent séparément sur les paniers **commande**, **réception** et **expédition**, avec support, confiance, lift et leverage.
- **0** décalage fournisseur, site, unité ou date de commande dans les 610 réceptions liées à leurs commandes exactes ; **0** ligne PO avec cumul de réception supérieur à 110 % parmi les unités comparables.
- **450 expéditions** conservées, dont 385 `delivered`, 34 `delayed`, 17 `in_transit`, 14 `returned`. Aucun temps de transit négatif dans les dates disponibles.
- **37** lignes d'ajustements avec référence d'expédition explicite : toutes retrouvées dans `shipments.csv`. Parmi ces références, **18** ajustements concernent un site qui n'est ni l'origine ni la destination déclarée, **17** une unité différente, **17** une catégorie différente. Ces alertes peuvent se chevaucher.
- **11** ajustements datés avant la réception référencée et **21** ajustements reliés à une réception d'un autre site.
- **47** lignes de stock mensuel présentent un écart absolu supérieur à 5 unités selon une formule simplifiée (sans garantie de couverture de tous les flux).
- **6** valeurs extrêmes IQR d'ajustements ; **3** partenaires atypiques à la fois selon LOF et Isolation Forest.

La table `erp_review_findings.csv` contient **140 alertes** (pas 140 incidents distincts) ; les fichiers `erp_adjustment_shipment_links.csv` et `erp_receipts_vs_purchase_orders.csv` permettent de vérifier les références de chacune.

## Cours 4 — Graphes et processus

- **2 460 nœuds** et **6 110 arêtes sourcées** : partenaires, sites, lignes PO, réceptions, jambes d'expédition, ajustements et inventaire mensuel.
- Centralités (degré, betweenness approchée), communautés Louvain, graphique du réseau partenaires/sites.
- **2 180 événements** pour le process mining : 650 commandes, 610 réceptions, 450 départs, 433 arrivées horodatées et 37 corrections reliées explicitement à une expédition. Les 17 expéditions sans arrivée sont `in_transit` et n'ont pas reçu de date artificielle.
- Deux familles de cas : `PO:...` et `SHP:...`. Elles ne sont **pas fusionnées** en l'absence d'une clé réception→expédition.

## à réaliser

Croiser `external_registration_number` avec les registres publics, `facility_name` / coordonnées avec les sites des autres domaines, et `shipment_number` avec les documents externes. Pour les événements de santé ou d'écologie, rapprocher dates et sites vérifiés **avec un groupe de contrôle**.
