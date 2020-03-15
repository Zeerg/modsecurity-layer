define build_layer
	docker run --name modsec -d modsec-layer false
	docker cp modsec:/opt layer
	docker rm modsec
	touch layer/.slsignore
endef

rebuild:
	docker build --no-cache --build-arg license=$(license) -t modsec-layer:latest .
	$(call build_layer)

build:
	docker build --build-arg license=$(license) -t modsec-layer:latest .
	$(call build_layer)

clean:
	rm -rf layer

deploy:
	serverless deploy