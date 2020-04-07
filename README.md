## ansodium
[Ansible Galaxy collection](https://galaxy.ansible.com/marmorag/ansodium) repository.\
Simple sodium wrapper module for `ansible`, based on [`PyNaCl`](https://pynacl.readthedocs.io/en/stable/)

### Install
---

Install it via ansible-galaxy (recommended):

```bash
ansible-galaxy collection install marmorag.ansodium
```
###### *__NOTE__: Installing collections with ansible-galaxy is only supported in ansible 2.9+*

You will need the `PyNacl` Python module to be installed.
```bash
pip install pynacl
```

Or use the provided `install` roles

---
Install it manually:

Refering to [ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-a-module-locally) to install a module, either :

- add directory to `ANSIBLE_LIBRARY` environment variable
- put it in  `~/.ansible/plugins/modules/`
- put in in `/usr/share/ansible/plugins/modules/`

```bash
git clone https://github.com/marmorag/ansodium 
cd ./ansodium

mkdir -p ~/.ansible/plugins/modules
cp ./ansodium.py ~/.ansible/plugins/modules
```

Or, to use it in one playbook/role only:

- put it in a `library` directory in the directory containing your __playbook__ 
- put it in a `library` directory in the directory containing your __role__ 

In any case, you can check that module is correctly installed with

```bash
ansible-doc -t module ansodium
```

Of course `PyNacl` python package is required in that case too.

### Usage

---

#### Generate keypair
```yaml
- name: generate keypair
  ansodium:
    keypair: true
```

Here `keypair` specify to generate a random keypair

Output format : 
```json
{
    "private_key": "<b64 encoded private key>",
    "public_key": "<b64 encoded public key>",
    "changed": true,
    "failed": false
}
```

---
#### Encrypt

```yaml
- name: encrypt data
  ansodium:
    pubkey: "<public key to encrypt with>"
    data: "<data you want to encrypt>"
```

Where `pubkey` and `data` is required.

Output format : 
```json
{
    "encrypted": "<encrypted data>",
    "original_data": "<original data>",
    "changed": true,
    "failed": false
}
```

---
#### Decrypt:

```yaml
- name: decrypt data
  ansodium:
    encrypt: false 
    prikey: "<private key to decrypt with>"
    data: "<data you want to decrypt>"
```

Where `prikey`, `data` and `encrypt` is required in order to decrypt data.  

Output format : 
```json
{
    "decrypted": "<decrypted data>",
    "original_data": "<original encrypted data>",
    "changed": true,
    "failed": false
}
```