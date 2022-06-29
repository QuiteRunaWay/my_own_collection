#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import os.path


def run_module():
    
    module_args = dict(
        file_name=dict(type='str', required=True),
        path=dict(type='str', required=True),
        content=dict(type='str', required=False)

    )

    
    result = dict(
        changed=False,
        original_message='',
        message=''
    )


    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    # file_name = 'Test_file.txt'

    full_path_file = module.params['path']+ '/' + module.params['file_name'] 
    
    if os.path.exists(full_path_file):
        result = dict(
            changed=False,
            original_message=full_path_file,
            message='File exist'
        )
    else:
        f = open(full_path_file, 'w+')
        if bool(module.params['content']) is True:
            f.write(module.params['content'])    
        f.close()
        result = dict(
            changed=True,
            original_message=full_path_file,
            message='File created'
        )

    

    if module.check_mode:
        module.exit_json(**result)


    # result['original_message'] = module.params['file_name']
    # # result['original_message'] = 'sjdfkjsdhgfjgsdfgs'
    # result['message'] = 'goodbye'


    # if module.params['new']:
    #     result['changed'] = True


    if module.params['file_name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)


    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
