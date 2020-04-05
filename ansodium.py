#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ansodium

short_description: Simple sodium encryption module

version_added: "X.X"

description:
    - "The main purpose of the module is to provide a simple access to sodium hash library."

options:
    keypair:
        description:
            - If you want to generate a keypair
        required: false
    pubkey:
        description:
            - The public key to encrypt your data with
        required: false
    prikey:
        description:
            - The private key to decrypt your data with
        required: false
    data:
        description:
            - Data you want to be encrypted
        required: false

author:
    - marmorag
'''

EXAMPLES = '''
# Encrypt data
- name: Test with a message
  ysodium:
    pubkey: asuperpubkey
    data: "a super set of data to be encrypted"
'''

RETURN = '''
original_data:
    description: The original data param that was passed in
    type: str
    returned: always
encrypted:
    description: The encrypted data that the module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from base64 import b64encode, b64decode

try:
    from nacl import encoding, public

    HAS_LIB = True
except ImportError:
    HAS_LIB = False


class AnsibleSodium:
    def __init__(self, module: AnsibleModule):
        self.module = module
        self.result = dict(
            changed=False,
            original_data='',
        )
        self.action = ''

    def run(self):
        if self.module.check_mode:
            self.module.exit_json(**self.result)

        if not HAS_LIB:
            self.module.fail_json(
                msg='pynacl library is required for this module. To install, use `pip install pynacl`')

        self.define_action()
        self.run_action()

        self.module.exit_json(**self.result)

    def define_action(self):
        if self.module.params['keypair']:
            self.action = 'keypair_generate'
        elif self.module.params['pubkey'] and self.module.params['encrypt']:
            self.action = 'asymetric_encrypt'
        elif self.module.params['prikey'] and not self.module.params['pubkey']:
            self.action = 'asymetric_decrypt'
        else:
            self.module.fail_json(msg='invalid parameters combination', **self.module.params)

    def run_action(self):
        action = getattr(self, self.action)
        action()

    def asymetric_encrypt(self):
        """Encrypt a Unicode string using the public key."""
        public_key = self.module.params['pubkey']
        secret_value = self.module.params['data']

        if len(secret_value) == 0:
            self.module.fail_json(msg='data is required to be encrypted')

        self.result['original_data'] = secret_value

        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

        self.result['encrypted'] = b64encode(encrypted).decode("utf-8")

        if self.result['encrypted'] != '':
            self.result['changed'] = True

    def asymetric_decrypt(self):
        private_key = self.module.params['prikey']
        secret_value = self.module.params['data']

        if len(secret_value) == 0:
            self.module.fail_json(msg='data is required to be decrypted')

        self.result['original_data'] = secret_value
        private_key = public.PrivateKey(private_key, encoding.Base64Encoder)
        sealed_box = public.SealedBox(private_key)
        decrypted = sealed_box.decrypt(b64decode(secret_value))

        self.result['decrypted'] = decrypted

        if self.result['decrypted'] == '':
            self.result['failed'] = True
        else:
            self.result['changed'] = True

    def keypair_generate(self):
        private_key = public.PrivateKey.generate()
        self.result['private_key'] = encoding.Base64Encoder.encode(bytes(private_key))
        self.result['public_key'] = encoding.Base64Encoder.encode(bytes(private_key.public_key))
        self.result['changed'] = True


def run_module():
    module_args = dict(
        keypair=dict(type='bool', required=False, default=False),
        pubkey=dict(type='str', required=False, default=""),
        prikey=dict(type='str', required=False, default=""),
        data=dict(type='str', required=False, default=""),
        encrypt=dict(type='bool', required=False, default=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    AnsibleSodium(module).run()


def main():
    run_module()


if __name__ == '__main__':
    main()
