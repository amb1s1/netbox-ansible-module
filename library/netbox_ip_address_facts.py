from ansible.module_utils.basic import *
import pynetbox


def main():

    module = AnsibleModule(
        argument_spec=dict(
          url=dict(type='str', required=True),
          token=dict(type='str', required=True),
          search=dict(type='str', required=True)
        ))
    model = 'ipam'
    obj = 'ip_addresses'
    url = module.params['url']
    token = module.params['token']
    search = module.params['search']
    nb = pynetbox.api(url, token=token)
    nb_model = getattr(nb, model)
    nb_obj = getattr(nb_model,  obj)
    search = nb_obj.get(q=search)
    if search:
        response = {
                    "ID": search.id,
                    "Status Value": search.status.value,
                    "Status Label": search.status.label,
                    "Description": search.description
                    }
    else:
        response = {
                    "ID": None,
                    "Status Value": None,
                    "Status Label": None,
                    "Description":  None
                    }
    module.exit_json(changed=False, meta=response)


if __name__ == "__main__":
    main()
