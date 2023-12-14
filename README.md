# NTCIR-17 UFO Text to Table Relationship Extraction サブタスク（Formal Run）

## 更新情報
- (2023/12/14) READMEの誤りの修正
- (2023/09/12) Gold Standardデータを公開しました。(`ufo_ttre_gs_20230530.json`)

# データセットについて
- TTRE の Formal Run では、Dry Run と同じデータを使用します。
- リーダーボード投稿の際にはバージョンとして Formal Run を指定してください。

## タスク設定
以下をご参照ください。
https://sites.google.com/view/ntcir17-ufo/subtasks/text-to-table-relationship-extraction

## 配布ファイル

このリポジトリには以下のファイルが含まれます。

- `training/**/*.ttre.html`
  - 各企業が発行した有価証券報告書に情報を追加したもので，trainingデータとして使用します。
  - 企業ごとにディレクトリ分けされています。
- `test/**/*.ttre.html`
  - 各企業が発行した有価証券報告書に情報を追加したもので，testデータとして使用します。
- `ttre_sample_output.py`
  - サンプルの推論スクリプトです。
  - ランダムにリンクセルIDを出力します。
- `sample_answer_sheet.json`
  - 提出用JSONファイルの書式サンプルです。
  - リンクセルIDを挿入すべきリストはすべて空になっています。
  - `ttre_sample_output.py`の出力形式もこの書式に準じています。
- `ttre_convert.py`
  - trainingデータの形式から提出用ファイル形式に変換します。
  - trainingデータの一部をdevデータとして使用したり，Gold Standardデータとして使用したりする場合にご活用ください。
- `ttre_eval.py`
  - 評価スクリプトです。各フレーズにおける `name/value`それぞれのPrecision，Recall，F1スコア，およびそれら3つのマクロ平均を出力します。
  - 引数として，`-g [Goldデータ.json] -i [システムの出力.json]` を指定してください。

## 入力ファイル形式

各企業が発行した有価証券報告書（HTML 形式）に，必要なアノテーションを行ったものを利用します。

### trainingデータ

`training/**/*.ttre.html`は，各企業が発行した有価証券報告書に以下の修正を加えたものです。

- `table`タグに `data-ttre-table-id`属性を追加。
  - `data-ttre-table-id`属性はテーブルを一意に識別する文字列で， `[書類管理番号]-[項目連番]-tab[テーブル連番]`の形式です。
- 各table内の `th`タグ， `td`タグに `data-ttre-cell-id`属性を追加。
  - `data-ttre-cell-id`属性はセルを一意に識別する文字列（セルID）で， `[書類管理番号]-[項目連番]-tab[テーブル連番]-r[行]c[列]` の形式です。
- `p`タグに `data-ttre-sentence-id`属性を追加。
  - `data-ttre-sentence-id`属性は段落を一意に識別する文字列で， `[書類管理番号]-[項目連番]-sent[段落連番]`の形式です。
- 各段落内の0個以上のフレーズに `mark`タグを追加。
  - `mark`タグによるフレーズは1つ以上のリンクセルがアノテータによって付与されています。
  - `data-ttre-mark-id`属性はフレーズを一意に識別する文字列で，`[書類管理番号]-[項目連番]-mark[フレーズ連番]`の形式です。
  - `data-ttre-name-cell-ids`属性は，アノテータによって関連があるとみなされた表における項目名に該当するセルIDが複数個（スペース区切り）付与されています。
  - `data-ttre-value-cell-ids`属性は，アノテータによって関連があるとみなされた表における値に該当するセルIDが複数個（スペース区切り）付与されています。
  - `data-ttre-etc-cell-ids`属性は，アノテータによって関連があるとみなされた表において，項目名にも値にも該当しないセルIDが複数個（スペース区切り）付与されています。本タスクでは検出対象外です。

### testデータ

`test/**/*.html`もtrainingデータ同様，各企業が発行した有価証券報告書に以下の修正を加えたものですが，以下の点が異なります。

- `mark`タグにおける3つのリンクセルに関する属性 `data-ttre-name-cell-ids, data-ttre-value-cell-ids, data-ttre-etc-cell-ids`の値を空白にしています。


## 出典

- `train` ならびに `test` ディレクトリ内のファイルは，EDINET 閲覧（提出）サイト（※）をもとに NTCIR-17 UFO タスクオーガナイザが作成したものです。
    - （※）例えば書類管理番号が `S100ISN0` の場合，当該ページの URL は `https://disclosure2.edinet-fsa.go.jp/WZEK0040.aspx?S100ISN0` となります。書類管理番号は，`train`/`test` ディレクトリ内の各ファイル名の先頭 8 文字です。
    - 各「提出本文書」の「第一部」を使用しています。
