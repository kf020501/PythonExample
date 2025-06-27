# ベースイメージ
FROM ubuntu:22.04

# 更新してPython 3.10、pip、およびGitをインストール
RUN apt-get update && \
    apt-get install -y \
        python3.10 \
        python3-pip \
        python3.10-venv \
        sudo \
        tree \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# locale設定(文字化け対策)
RUN apt-get update && apt-get install -y locales && \
    sed -i 's/# ja_JP.UTF-8 UTF-8/ja_JP.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen ja_JP.UTF-8

ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8

# 非rootユーザーを作成・切り替え、作業ディレクトリを設定
RUN useradd -m -s /bin/bash user && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER user
WORKDIR /home/user/src

# Pythonパッケージのインストール(venv)
COPY requirements.txt /home/user
RUN python3 -m venv /home/user/venv && \
    /home/user/venv/bin/pip install --no-cache-dir -r /home/user/requirements.txt

# シェル起動時に venv を有効化
RUN echo "source /home/user/venv/bin/activate" >> /home/user/.bashrc

# コマンド
CMD ["/bin/bash"]