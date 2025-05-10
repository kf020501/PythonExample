# Dockerイメージ名とタグを変数に設定
IMAGE_NAME := python-dev-ubuntu22.04
TAG := latest
WORK_DIR := .

.PHONY: build run

# Dockerイメージのビルド
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Dockerコンテナの起動
run:
	docker run -v $(WORK_DIR):/home/user/work -it --rm $(IMAGE_NAME):$(TAG)

# イメージの削除
clean:
	docker rmi $(IMAGE_NAME):$(TAG) || true

# Docker状況確認
show:
	docker images
	docker ps -a