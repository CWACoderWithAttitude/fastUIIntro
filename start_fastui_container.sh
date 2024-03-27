#!/bin/sh
ext_port="3800"
tag="fastui-startrek:0.2"
docker run -p ${ext_port}:8000 -t $tag
