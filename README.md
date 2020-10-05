## ansodium
[Ansible Galaxy collection](https://galaxy.ansible.com/marmorag/ansodium) repository.\
Simple sodium wrapper module for `ansible`, based on [`PyNaCl`](https://pynacl.readthedocs.io/en/stable/)

### My use case

In order to automate some Github related things, I have to use the [`Actions/Secrets`](https://developer.github.com/v3/actions/secrets/) endpoint.
To create or update a secrets I needed to encrypt data using the [Sodium library](https://libsodium.gitbook.io/doc/) and I found nothing `Ansible` related to do that.
Firstly I created a `NodeJS` script with [tweetsodium](https://github.com/github/tweetsodium), but it was not really usable in `Ansible` context.
So, ... I writed down a module. For now it is deadly simple, it just generate Keypair, encrypt and decrypt, but it works.


If you want an example of what it looks like, then this is the roles which embbed it:
```yaml
- name: Github - fetch project public key
  uri:
    url: "{{ github_api_repo_url }}/actions/secrets/public-key"
    headers:
      Authorization: "token {{ github_personnal_token }}"
    status_code: 200
  register: github_pubkey

- name: Github - Encrypt token
  ansodium:
    pubkey: "{{ github_pubkey.json.key }}"
    data: "{{ secret_token }}"
  register: encrypt_output

- name: Github - Push new secrets
  uri:
    url: "{{ github_api_repo_url }}/actions/secrets/SECRET_TOKEN"
    body:
      encrypted_value: "{{ encrypt_output.encrypted }}"
      key_id: "{{ github_pubkey.json.key_id }}"
    body_format: json
    method: PUT
    status_code: 201,204
    headers:
      Authorization: "token {{ github_personnal_token }}"
```

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

```yaml
roles:
    - { role: marmorag.ansodium.install }
```

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