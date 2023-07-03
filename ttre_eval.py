from __future__ import annotations

"""
UFO TTREタスクの評価スクリプト。
使い方：
    [-i] 推定結果ファイル
    [-g] Gold Standardファイル
出力：
    標準出力に評価結果がJSON形式で出力される。
作成：2023/03/23 乙武北斗
"""

import argparse
import json
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class EvalResult:
    """
    評価結果のスキーマ
    """
    success: bool
    name_f1: float
    value_f1: float
    total_f1: float
    marks: dict[str, dict[str, dict[str, int | float | None]]]


@dataclass
class PhraseEvals:
    org: int
    est: int
    crr: int

    def precision(self) -> float | None:
        if self.est == 0:
            return None
        return self.crr / self.est

    def recall(self) -> float | None:
        if self.org == 0:
            return None
        return self.crr / self.org

    def f1(self) -> float | None:
        p = self.precision()
        r = self.recall()
        if p is None and r is None:
            return None
        if p is None or r is None:
            return 0
        if p + r == 0:
            return 0
        return (2 * p * r) / (p + r)

    def to_dict(self) -> dict[str, int | float | None]:
        return {
            "org": self.org,
            "est": self.est,
            "crr": self.crr,
            "precision": self.precision(),
            "recall": self.recall(),
            "f1": self.f1()
        }


def get_args():
    """
    コマンドライン引数を処理する関数．
    [-i] 推定結果ファイル
    [-g] Gold Standardファイル
    """
    parser = argparse.ArgumentParser(
        description="""UFO TTREタスクの評価スクリプト。"""
    )

    parser.add_argument("-i", "--input", required=True,
                        help="推定結果ファイルを指定します")
    parser.add_argument("-g", "--gs", required=True,
                        help="Gold Standardファイルを指定します")
    return parser.parse_args()


if __name__ == "__main__":
    # コマンドライン引数の解析
    args = get_args()

    evals = EvalResult(True, 0, 0, 0, {})
    name_phrases: list[PhraseEvals] = []
    value_phrases: list[PhraseEvals] = []
    result: dict[str, dict[str, list[str]]] = json.loads(
        Path(args.input).read_text(encoding="utf-8"))
    gs: dict[str, dict[str, list[str]]] = json.loads(
        Path(args.gs).read_text(encoding="utf-8"))

    for mid, anss in gs.items():
        if mid not in result:
            evals.success = False
            break

        n = PhraseEvals(
            org=len(anss["name"]),
            est=len(result[mid]["name"]),
            crr=len(set(anss["name"]) & set(result[mid]["name"]))
        )
        v = PhraseEvals(
            org=len(anss["value"]),
            est=len(result[mid]["value"]),
            crr=len(set(anss["value"]) & set(result[mid]["value"]))
        )
        name_phrases.append(n)
        value_phrases.append(v)

        evals.marks[mid] = {
            "name": n.to_dict(),
            "value": v.to_dict()
        }

    if evals.success:
        nf1s = [y for x in name_phrases if (y := x.f1()) is not None]
        evals.name_f1 = sum(nf1s) / len(nf1s)
        vf1s = [y for x in value_phrases if (y := x.f1()) is not None]
        evals.value_f1 = sum(vf1s) / len(vf1s)
        evals.total_f1 = (evals.name_f1 + evals.value_f1) / 2
        print(json.dumps(asdict(evals), ensure_ascii=False, indent=4))
    else:
        print(json.dumps(asdict(evals), ensure_ascii=False, indent=4))
