from __future__ import annotations

"""
UFO TTREタスクのtrainingデータの形式から，提出用のファイル形式に返還します。
依存ライブラリ：
    HTML解析ライブラリのBeautifusoup4を使用します。
    pip install beautifulsoup4
    などでインストールしてください。
使い方：
    [-i] 資料HTMLファイル（複数指定）
出力：
    標準出力に提出用JSON形式で出力される。
作成：2023/04/24 乙武北斗
"""

import argparse
import json
from pathlib import Path
from bs4 import BeautifulSoup


def get_args():
    """
    コマンドライン引数を処理する関数．
    [-i] 資料HTMLファイルを含むディレクトリを指定する。
    """
    parser = argparse.ArgumentParser(
        description="""UFO TTREタスクの推論スクリプトサンプル。
ランダムにセルIDを付与する。"""
    )

    parser.add_argument("-i", "--input-files", nargs="+", required=True,
                        help="資料HTMLファイルを指定します")
    return parser.parse_args()


def get_mark_info(src: BeautifulSoup) -> dict[str, dict[str, list[str]]]:
    ret = {}
    marks = src.select("mark.annotate")
    for t in marks:
        ret[t.attrs["data-ttre-mark-id"]] = {
            "name": sorted(t.attrs.get("data-ttre-name-cell-ids", "").split()),
            "value": sorted(t.attrs.get("data-ttre-value-cell-ids", "").split()),
            "etc": sorted(t.attrs.get("data-ttre-etc-cell-ids", "").split()),
        }
    return ret


if __name__ == "__main__":
    args = get_args()
    results: dict[str, dict[str, list[str]]] = {}

    for html_file in [Path(x) for x in args.input_files]:
        bs = BeautifulSoup(html_file.read_text(
            encoding="utf-8"), "html.parser")
        results.update(get_mark_info(bs))

    print(json.dumps(results, ensure_ascii=False, indent=4))
