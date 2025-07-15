# SMB Share Provisioning & ACL Management with Ansible on ONTAP

## Goals

- Provision a new SMB share via Ansible playbook.
- Remove the default "Everyone / Full Control" permission from the top-level directory after share creation.

This repository contains Ansible playbooks and supporting scripts for managing SMB shares and NTFS ACLs on NetApp ONTAP systems.  
Key capabilities include:

- **Provisioning SMB shares** and displaying volume/share info (`vol_share_info.yml`)
- **Setting NTFS ACLs** on top-level directories (`set_new_acls.yml`)
- **Querying and displaying NTFS ACLs** via ONTAP REST API (`show_ntfs_acls.yml`)
- **Reference and troubleshooting notes** for REST API usage and encoding requirements


## Next Steps / TODO

- Add playbooks to **remove default "Everyone / Full Control" ACL** after share creation
- Add error handling and validation for path encoding and security style
- Parameterize domain, SVM, and share names for easier reuse
- Integrate reporting (e.g., export ACLs to CSV or HTML)
- Add more examples for subdirectory ACL management
- Document REST API quirks and encoding requirements for future users


## References

- [ONTAP Ansible Collection](https://galaxy.ansible.com/netapp/ontap)
- [ONTAP REST API Documentation](https://<ONTAP_IP>/docs/api)
- [Netapp.ONTAP Ansible Documentation](https://docs.ansible.com/ansible/latest/collections/netapp/ontap/index.html#plugins-in-netapp-ontap)