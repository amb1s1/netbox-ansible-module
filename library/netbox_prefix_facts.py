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
    obj = 'prefixes'
    url = module.params['url']
    token = module.params['token']
    search = module.params['search']
    nb = pynetbox.api(url, token=token)
    nb_model = getattr(nb, model)
    nb_obj = getattr(nb_model,  obj)
    prefix = nb_obj.get(q=search)
    response = {"Next Available IP": prefix.available_ips.list()[0]['address'],
                "Next Available Range": prefix.available_ips.list(),
                "ID": prefix.id,
                "Status Value": prefix.status.value,
                "Status Label": prefix.status.label,
                "Description": prefix.description
                }
    module.exit_json(changed=False, meta=response)


if __name__ == "__main__":
    main()
