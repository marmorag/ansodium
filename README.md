## ansodium
Simple sodium wrapper module for ansible, based on [`PyNaCl`](https://pynacl.readthedocs.io/en/stable/)

### Install

Refering to [ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-a-module-locally) to install a module locally, either :

- add directory to `ANSIBLE_LIBRARY` environment variable
- put it in  `~/.ansible/plugins/modules/`
- put in in `/usr/share/ansible/plugins/modules/`

```bash
git clone git@github.com:/marmorag/ansodium.git 
cd ./ansodium

mkdir -p ~/.ansible/plugins/modules
cp ./ansodium.py ~/.ansible/plugins/modules
```

then you can check that module is correctly installed with

```bash
ansible-doc -t module ansodium
```

### Usage

---

#### Generate keypair
```yaml
- name: run the module
  ansodium:
    keypair: true
```

Where `pubkey` and `data` is required.

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
- name: run the module
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
- name: run the module
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