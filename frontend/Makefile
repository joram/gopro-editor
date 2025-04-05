build_api_client:
	sudo rm -r api-client || true
	sudo rm -r src/api-client || true
	cd src;	wget http://localhost:8000/openapi.json -O ./openapi.json
	docker pull openapitools/openapi-generator-cli:latest
	cd src; docker run --rm \
		--network veilstream-network \
		-v ./:/local \
		openapitools/openapi-generator-cli:latest generate \
			-i /local/openapi.json \
			-g typescript-axios \
			-o /local/api-client
	sudo chown ${USER}:${USER} -R src/api-client
	sudo chmod 755 -R src/api-client