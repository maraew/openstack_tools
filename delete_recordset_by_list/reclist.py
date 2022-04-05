#Author Yaroslav Isakov (c)
import json
import openstack
from designateclient.v2 import client
from designateclient.v2.utils import get_all
conn = openstack.connect()
dns_client = client.Client(session=conn.session, all_projects=True)
all_zones = get_all(dns_client.zones.list)
arpa_zones = [zone['id'] for zone in all_zones if zone['name'].endswith('.in-addr.arpa.')]
a_zones = [zone['id'] for zone in all_zones if zone['name'].endswith('.booking.com.')]
all_ptrs = {}
all_a = {}
#t = get_all(dns_client.recordsets.list, args={a_zones[0]})
#from pdb import set_trace; set_trace()
for zone in a_zones:
   all_a.update({record['records'][0]: (record['zone_id'], record['name'], record['created_at'], record['updated_at']) for record in get_all(dns_client.recordsets.list, args={zone}) if record["type"]=="A"})
for zone in arpa_zones:
   all_ptrs.update({".".join(reversed(record['name'].split(".")[:4])): (record['zone_id'], record['records'][0], record['created_at'], record['updated_at']) for record in get_all(dns_client.recordsets.list, args={zone}) if record["type"]=="PTR"})
fips = conn.network.ips()
all_fips = set([fip.floating_ip_address for fip in fips])
print "Extra PTRS"
extra_ptrs = {k: v for k, v in all_ptrs.items() if k not in all_fips}
print json.dumps(extra_ptrs, indent=4)
print "Extra A"
extra_a = {k: v for k, v in all_a.items() if k not in all_fips}
print json.dumps(extra_a, indent=4)
all_extra_fips = set(extra_a.keys()).union(set(extra_ptrs.keys()))
not_matching_fips = set()
for fip in all_extra_fips:
    try:
        if extra_ptrs[fip][1] != extra_a[fip][1]:
            print "Not matching", fip, extra_ptrs[fip][1], extra_a[fip][1]
            not_matching_fips.add(fip)
    except KeyError:
        not_matching_fips.add(fip)
print not_matching_fips

