# [netapp-lod-sandbox](https://github.com/KenHillier/netapp-lod-sandbox.git)

A collection of scripts and notes used to test NetApp features and APIs


## GIT Setup

```bash
### Variables
GIT_USER_NAME="Ken Hillier"
GIT_USER_EMAIL="ken.hillier@gmail.com"

### Update Git global configuration
git config --global user.name "$GIT_USER_NAME"
git config --global user.email "$GIT_USER_EMAIL"
git config --global pull.rebase true

echo "Git global configuration updated:"
git config --global --get user.name
git config --global --get user.email
git config --global --get pull.rebase

### Add the current directory to the PATH
export PATH=$PATH:.
```