from ansible.module_utils.basic import AnsibleModule
import pynetbox
import json

search_type = dict(
    prefixes="q",
    ip_addresses="q",
    devices="name",
    device_types="slug",
    device_roles="slug",
    sites="slug",
)


def find_id(nb_model, obj, search):
    nb_obj = getattr(nb_model, obj)
    results = nb_obj.get(**{search_type.get(obj, "q"): search})
    if results:
        return results.id
    else:
        return 1


def netbox_add(nb_model, nb_obj, data):
    clean_json = data.replace("'", '"')
    data = json.loads(clean_json)
    site = find_id(nb_model, "sites", data.get("site"))
    device_role = find_id(nb_model, "device_roles", data.get("device_role"))
    device_type = find_id(nb_model, "device_types", data.get("device_type"))
    data["status"] = 1 if data.get("status") == "active" else 0
    data["site"] = site
    data["device_role"] = device_role
    data["device_type"] = device_type
    try:
        return [nb_obj.create([data])]
    except pynetbox.RequestError as e:
        return e.error


def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type="str", required=True),
            token=dict(type="str", required=True),
            data=dict(type="str", required=False),
            action=dict(type="str", required=False),
            model=dict(type="str", required=True),
            obj=dict(type="str", required=True),
        )
    )
    model = module.params["model"]
    obj = module.params["obj"]
    url = module.params["url"]
    token = module.params["token"]
    data = module.params["data"]
    action = module.params["action"]
    nb = pynetbox.api(url, token=token)
    nb_model = getattr(nb, model)
    nb_obj = getattr(nb_model, obj)
    response = netbox_add(nb_model, nb_obj, data)

    module.exit_json(changed=False, meta=response)


if __name__ == "__main__":
    main()
