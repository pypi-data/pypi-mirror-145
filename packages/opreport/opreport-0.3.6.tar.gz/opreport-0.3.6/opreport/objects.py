def get_objects(openv, obtype, queryString=None, searchQuery=None,countonly=False, attrId=None, tenant=None, partner=None):
    if tenant is None:
        tenant = openv.env['tenant']
    if partner is None:
        partner = openv.env['partner']

    endpoints = {
        "clients": f'/api/v2/tenants/{partner}/clients/tenant',
        "incidentCustomFields": f'/api/v2/tenants/{tenant}/customFields/INCIDENT',
        "deviceGroups": f'/api/v2/tenants/{tenant}/deviceGroups/minimal',
        "users": f'/api/v2/tenants/{tenant}/users/search',
        "userGroups": f'/api/v2/tenants/{tenant}/userGroups',
        "urgencies": f'/api/v2/tenants/{tenant}/incidents/urgencies',
        "customAttributes": f'/api/v2/tenants/{tenant}/customAttributes/search',
        "resources": f'/api/v2/tenants/{tenant}/resources/search',
        "resourcesNewSearch": f'/api/v2/tenants/{tenant}/query/execute',
        "assignedAttributeEntities": f'/api/v2/tenants/{tenant}/customAttributes/{str(attrId)}/assignedEntities/search',
        "consoleRecordings": f'/api/v2/tenants/{tenant}/resources/auditRecordings/search'
    }

    url = endpoints[obtype]

    return openv.do_get(url, 1, queryString, searchQuery, countonly, attrId)
    
def get_object(openv, obtype, id, tenant=None, partner=None):
    if tenant is None:
        tenant = openv.env['tenant']
    if partner is None:
        partner = openv.env['partner']

    endpoints = {
        "resource": f'/api/v2/tenants/{tenant}/resources/{id}',
        "discoveredApps": f'/api/v2/tenants/{tenant}/resources/{id}/applications',
        "discoveredServices": f'/api/v2/tenants/{tenant}/resources/{id}/discoveredServices',
    }

    url = endpoints[obtype]

    paginate = True
    pagebug = False
    if obtype == 'discoveredApps':
        paginate = False
    if obtype == 'discoveredServices':
        pagebug = True
    return openv.do_get(url, paginate=paginate, pagebug=pagebug)