from ansible.module_utils.basic import AnsibleModule
import pynetbox


search_type = dict(prefixes="iq", ip_addresses="iq", devices="name", sites="iq")


def facts(obj, nb_obj, search):
    if search_type.get(obj, "iq") is "iq":
        if search:
            results = nb_obj.get(q=search)
        else:
            results = nb_obj.all()
    elif search_type.get(obj) is "name":
        results = nb_obj.get(name=search)
    response = dict()
    if results:
        if search:
            for result in results:
                response[result[0]] = result[1]
        else:
            for result in results:
                for item in result:
                    response[item[0]] = item[1]

    else:
        response["item"] = None
    return response


def main():

    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type="str", required=True),
            token=dict(type="str", required=True),
            search=dict(type="str", required=False),
            action=dict(type="str", required=False),
            model=dict(type="str", required=True),
            obj=dict(type="str", required=True),
        )
    )
    model = module.params["model"]
    obj = module.params["obj"]
    url = module.params["url"]
    token = module.params["token"]
    search = module.params["search"]
    nb = pynetbox.api(url, token=token)
    nb_model = getattr(nb, model)
    nb_obj = getattr(nb_model, obj)
    response = facts(obj, nb_obj, search)

    module.exit_json(changed=False, meta=response)


if __name__ == "__main__":
    main()
