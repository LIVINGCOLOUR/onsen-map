# クラウド実行の調べ直し（共通）

このリポジトリ（かけ流し日帰りマップ）の data.json に、日帰りで入れる源泉かけ流しの温泉を集めている。
まず research/brief/common.md と research/brief/region.md を読み、収録基準・項目の書き方・塩素の基準・座標・個人情報の決まりに従う。checkedAt は "2026-11-05"。
ブリーフ中の「scratchpad/<担当名>」は、クラウド実行では **research/cloud/<担当名>/** と読み替える（出力ファイルもそこに置く）。

## 守ること
- data.json と index.html は**変更しない**（読むだけ）。結果は research/cloud/<担当名>/ のファイルだけ。
- 外部へのリクエストに個人情報（メールアドレスなど）を入れない。汎用の User-Agent を使う。
- 源泉バンク (gensenbank.com) は手がかりのみ。/api は読まない。1秒以上あけて読む。
- WebSearch は多くても20回。一覧ページや公式サイトは curl で直接読む。
- hasSauna は全件 "あり"|"なし"（ニフティ施設ページ https://onsen.nifty.com/a/onsenNNNNNN/ の HTML で、saunaIconClick のボタンの class に is-disabled があれば「なし」）。
- id は data.json と重複させない（同じ施設がすでにあれば「既収録」）。
- 時間の上限がある（約3時間）。2時間半を過ぎたら、途中でもそこまでの結果をファイルに書いて push する。

## 出力
- research/cloud/<担当名>/new.json: 新たに収録する項目（data.json の items と同じ形）
- research/cloud/<担当名>/updates.json: 既収録の修正 [{id, name, set:{...}, evidenceAdd, reason}]、削除は {id, name, delete:true, reason}（caveats を set するときは既存文を含めた全文）
- research/cloud/<担当名>/checked.json: 確かめた候補全件 {name, address, source, verdict: 収録|除外|保留|既収録, reason, id, tel}
- research/cloud/<担当名>/call.md: 電話で聞けば決まる保留（施設名・電話・聞くこと）
- research/cloud/<担当名>/report.md: 確かめた件数・判定の内訳・収録分の塩素の内訳・注意点・使った検索回数

## 最後に
ブランチ `cloud/<担当名>` を作ってコミットし、push する（main には push しない）。
