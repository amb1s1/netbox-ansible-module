#!/usr/bin/python

ANSIBLE_METADATA = {
    "metadata_version": "0.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: netbox

short_description: Netbox Module

version_added: "2.4"

description:
    - Show netbox information 

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false


author:
    - David Gomez (david.gomez@networktocode.com)
"""

EXAMPLES = """
- name: Get site information
  netbox:
    module: dcim
    obj: sites
    search: LAX

- name: Get IP Address information
  netbox:
    module: ipam
    obj: ip_addresses
    search: 10.0.0.1/24

- name: Show Prefix
  netbox:
    module: ipam
    obj: prefixes
    search: 10.0.0.0/24
"""

RETURN = """
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
"""
from ansible.module_utils.basic import AnsibleModule
import pynetbox


search_type = dict(
    prefixes="q",
    ip_addresses="q",
    devices="name",
    device_types="slug",
    device_roles="slug",
    sites="q",
)


def facts(obj, nb_obj, search):

    if search:
        results = nb_obj.get(**{search_type.get(obj, "q"): search})
    else:
        results = nb_obj.all()
    response = []
    facts_dict = dict()
    if results:
        if search:
            for result in results:
                facts_dict[result[0]] = result[1]
            response.append(facts_dict)
        else:
            for result in results:
                for item in result:
                    facts_dict[item[0]] = item[1]
                response.append(facts_dict)
                facts_dict = dict()
    else:
        response["item"] = None
    return response


def main():

    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type="str", required=True),
            token=dict(type="str", required=True),
            search=dict(type="str", required=False),
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
