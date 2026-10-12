"""Tests de cohérence sur la livraison logistique à sept jeux de données."""
from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parent
csv=lambda folder,name:pd.read_csv(root/'data'/folder/(name+'.csv'))
expected_raw={'erp_business_partners':80,'erp_facilities':30,'purchase_order_lines':651,
              'goods_receipts':612,'shipments':452,'inventory_adjustments':140,'inventory_month_end':502}
expected_clean={'erp_business_partners':80,'erp_facilities':30,'purchase_order_lines':650,
                'goods_receipts':610,'shipments':450,'inventory_adjustments':140,'inventory_month_end':500}
for name,rows in expected_raw.items():
 assert len(csv('raw',name))==rows,(name,'raw')
 assert len(csv('part1_clean',name+'_clean'))==expected_clean[name],(name,'clean')
assert csv('part1_clean','referential_integrity').nombre.sum()==0
r=csv('part3_patterns','erp_receipts_vs_purchase_orders'); assert r.found_po.all() and len(r)==610
s=csv('part3_patterns','erp_adjustment_shipment_links');assert len(s)==37 and s.found_shipment.all()
a=csv('part3_patterns','erp_review_findings');assert len(a)>0 and a.record_id.notna().all()
assert (a.rule_id=='stock_variance_gt5').sum()==csv('part3_patterns','inventory_reconciliation').flag_variance_gt5.sum()
gn=csv('part4_graph','erp_graph_nodes');ge=csv('part4_graph','erp_graph_edges')
assert gn.node_id.is_unique and ge.source_id.isin(gn.node_id).all() and ge.target_id.isin(gn.node_id).all()
assert set(['ORDER_LINE','SHIPMENT_LEG','RECEIPT','ADJUSTMENT']).issubset(set(gn.node_type))
events=csv('part4_graph','erp_process_event_log')
assert 'shipment_dispatched' in events.activity.values and 'shipment_arrived' in events.activity.values
assert len(csv('part4_graph','erp_cross_domain_export'))==len(a)
print('OK — 7 datasets, 4 notebooks, intégrité PO/shipments, alertes, graphes, process mining et exports groupe.')
