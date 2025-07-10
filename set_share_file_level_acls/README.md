# SMB Share Provisioning & ACL Management with Ansible on ONTAP

This prototype demonstrates how to provision an SMB share on NetApp ONTAP using Ansible, with a focus on managing top-level directory ACLs.

## Goals

- Provision a new SMB share via Ansible playbook.
- Remove the default "Everyone / Full Control" permission from the top-level directory after share creation.

## Usage

1. Use the provided Ansible playbook to create the SMB share.
2. Apply file-level ACL changes to restrict permissions as required.

## References

- [ONTAP Ansible Collection](https://galaxy.ansible.com/netapp/ontap)
- [ONTAP REST API Documentation](https://<ONTAP_IP>/docs/api)
- [Netapp.ONTAP Ansible Documentation](https://docs.ansible.com/ansible/latest/collections/netapp/ontap/index.html#plugins-in-netapp-ontap)