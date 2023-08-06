#!/usr/bin/env bash

docker run \
    -it \
	--rm \
	-v $(pwd):/io \
	-e PATH=/opt/python/cp37-cp37m/bin:/opt/python/cp38-cp38/bin:/opt/python/cp39-cp39/bin:/opt/python/cp310-cp310/bin:/root/.cargo/bin:/opt/rh/devtoolset-8/root/usr/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
	ghcr.io/pyo3/maturin:v0.12.11 \
	build --release 

