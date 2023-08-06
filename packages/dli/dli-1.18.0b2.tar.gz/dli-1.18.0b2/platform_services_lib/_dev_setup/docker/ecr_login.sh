SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
$SCRIPT_DIR/octo_latest_linux_amd64/octo login aws --profile octo
aws ecr get-login-password --region eu-west-1 --profile octo | docker login --username AWS --password-stdin 116944431457.dkr.ecr.eu-west-1.amazonaws.com
