from irrd.storage.database_handler import DatabaseHandler
from irrd.storage.queries import RPSLDatabaseQuery
from irrd.conf import config_init

config_init('/etc/irrd.yaml')

dh = DatabaseHandler()
q = RPSLDatabaseQuery(column_names=['rpsl_pk', 'source', 'parsed_data'], ordered_by_sources=False, enable_ordering=False)
q = q.object_classes(['mntner']).sources(['NTTCOM'])
mntners = dh.execute_query(q)
some_mixed = [
    mntner
    for mntner in mntners
    if not all([
        auth.split(' ')[0].isupper()
        for auth in mntner['parsed_data'].get('auth', [])
    ])
]
print('Potentialy affected objects:')
for i in some_mixed:
    print('-------')
    print(i)
dh.close()
