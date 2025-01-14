echo "Setting up Vault..."
export VAULT_ADDR=https://vault.control.acceleratorlabs.ca
export VAULT_TOKEN=$(vault write -field=token auth/approle/login role_id=d947ef1f-956f-b24c-929f-9c240f777ed6 secret_id=7c832748-4422-cc3b-17ce-33c499bd950e)

echo "Setting up gcloud..."
export GOOGLE_APPLICATION_CREDENTIALS=$(mktemp)
vault read -field=private_key_data gcp/roleset/keith-m-leung/key | base64 -d > /Users/kleung132/Documents/Training/PoC/poc/sa_key.json
sleep 3
gcloud auth activate-service-account --key-file=/Users/kleung132/Documents/Training/PoC/poc/sa_key.json
