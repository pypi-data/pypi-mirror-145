try:
    from paraview import servermanager
except:
    pass


def unwrap(obj):
    if hasattr(obj, "SMProxy"):
        obj = obj.SMProxy
    if hasattr(obj, "SMProperty"):
        obj = obj.SMProperty
    return obj


def id_to_proxy(poxy_id):
    try:
        poxy_id = int(poxy_id)
    except:
        return None
    if poxy_id <= 0:
        return None
    return servermanager._getPyProxy(
        servermanager.ActiveConnection.Session.GetRemoteObject(poxy_id)
    )
