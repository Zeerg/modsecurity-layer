define build_layer
	docker run --name modsec -d modsec-layer false
	docker cp modsec:/opt layer
	docker rm modsec
	touch layer/.slsignore
	echo "**/*.la" > layer/.slsignore
	echo "share/**" >> layer/.slsignore
	echo "include/**" >> layer/.slsignore
	echo "bin/**" >> layer/.slsignore
endef

rebuild:
	docker build --no-cache -t modsec-layer:latest .
	$(call build_layer)

build:
	docker build -t modsec-layer:latest .
	$(call build_layer)

clean:
	rm -rf layer

deploy:
	serverless deploy