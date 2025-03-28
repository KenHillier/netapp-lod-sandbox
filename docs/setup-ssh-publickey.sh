#!/bin/bash

# Description: Set ONTAP cluster admin public key to bypass password prompt
# Create and setup a public key for the ONTAP cluster admin account to bypass the password prompt when running ONTAP commands.

# Variables
KEY_PATH="/root/.ssh/id_rsa"
CLUSTER_USER="admin"
CLUSTER_HOST="cluster1"
VSERVER="cluster1"
ADMIN_USER="admin"

echo ============================================
echo "Setting up SSH Publickeys for ONTAP Cluster Admin"
date
echo ============================================

# Generate SSH key pair if it doesn't exist
if [ ! -f "$KEY_PATH" ]; then
    ssh-keygen -t ecdsa -b 521 -C "admin@demo.netapp.com" -f "$KEY_PATH" -N ""
fi

# Read the public key
PUBLIC_KEY=$(cat "${KEY_PATH}.pub")

# Create ONTAP cluster admin login with public key authentication
echo "ssh ${CLUSTER_USER}@${CLUSTER_HOST} \"security login create -user-or-group-name admin -application ssh -authentication-method publickey -role admin -vserver ${CLUSTER_HOST}\""
ssh ${CLUSTER_USER}@${CLUSTER_HOST} "security login create -user-or-group-name admin -application ssh -authentication-method publickey -role admin -vserver ${CLUSTER_HOST}"

# Add the public key to the ONTAP cluster
echo "ssh ${CLUSTER_USER}@${CLUSTER_HOST} \"security login publickey create -vserver ${VSERVER} -username ${ADMIN_USER} -publickey ${PUBLIC_KEY}\""
# ssh ${CLUSTER_USER}@${CLUSTER_HOST} "security login publickey create -vserver ${VSERVER} -username ${ADMIN_USER} -publickey '${PUBLIC_KEY}'"  # Original with `` causing error
ssh ${CLUSTER_USER}@${CLUSTER_HOST} "security login publickey create -vserver ${VSERVER} -username ${ADMIN_USER} -publickey \"${PUBLIC_KEY}\""

# Show the public keys for the admin user
echo "ssh ${CLUSTER_USER}@${CLUSTER_HOST} \"security login publickey show -username admin\""
ssh ${CLUSTER_USER}@${CLUSTER_HOST} "security login publickey show -username admin"

###################################################

echo ============================================
echo "Script execution completed."
date
echo ============================================