from __future__ import annotations

"""
UFO TTREタスクの推論スクリプトサンプル。
ランダムにセルIDを付与する。
依存ライブラリ：
    HTML解析ライブラリのBeautifusoup4を使用します。
    pip install beautifulsoup4
    などでインストールしてください。
使い方：
    [-i] 資料HTMLファイル（複数指定）
出力：
    標準出力に推論結果がJSON形式で出力される。
更新：2023/04/24 [-i]オプションの形式を変更
更新：2023/04/05 属性名の修正
作成：2023/03/23 乙武北斗
"""

import argparse
import random
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


def get_cell_ids(src: BeautifulSoup) -> list[str]:
    """
    指定したHTMLに含まれる表のセルからすべてのセルIDを取得する。
    """
    cells = src.select("*[data-ttre-cell-id]")
    return [t.attrs["data-ttre-cell-id"] for t in cells]


def get_mark_ids(src: BeautifulSoup) -> list[str]:
    """
    指定したHTMLの文に含まれるすべてのリンクフレーズのMark IDを取得する。
    """
    marks = src.select("mark.annotate")
    return [t.attrs["data-ttre-mark-id"] for t in marks]


if __name__ == "__main__":
    # コマンドライン引数の解析
    args = get_args()

    # 結果オブジェクト
    results: dict[str, dict[str, list[str]]] = {}

    for html_file in [Path(x) for x in args.input_files]:
        bs = BeautifulSoup(html_file.read_text(
            encoding="utf-8"), "html.parser")
        cell_ids = get_cell_ids(bs)
        for mark_id in get_mark_ids(bs):
            results[mark_id] = {
                "name": random.sample(cell_ids, random.randint(0, 5)),
                "value": random.sample(cell_ids, random.randint(0, 5))
            }

    print(json.dumps(results, ensure_ascii=False, indent=4))
