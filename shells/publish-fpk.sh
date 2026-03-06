target=$(cd $(dirname $0)/..; pwd)

mkdir -p public/publish-fpk/docker
cp -rf install-package/fpk/docker/* public/publish-fpk/docker

sed -i "s|{version}|1.0.8|g" public/publish-fpk/docker/manifest
sed -i "s|{changelog}|1. 一些累计更新，写了一些新bug、2. 加入可选登录限制，是否必须登录飞牛才能打开应用|g" public/publish-fpk/docker/manifest
sed -i "s|{version}|v1.0.8|g" public/publish-fpk/docker/app/docker/docker-compose.yaml
sed -i 's/\r$//' public/publish-fpk/docker/manifest
sed -i 's/\r$//' public/publish-fpk/docker/cmd/main
sed -i 's/\r$//' public/publish-fpk/docker/cmd/uninstall_callback

cd public/publish-fpk/docker

tar -czf app.tgz --transform='s,app/,,g' app/docker app/www app/ui config
tar -czf fnpackup.fpk --exclude='app' *
mv fnpackup.fpk fnpackup-docker.fpk
