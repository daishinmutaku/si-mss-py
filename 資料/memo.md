- [ ] FPRの評価
  - [x] 10000 回実験
  - [x] selective-p が一様分布になるか確認 → Kolmogorov-Smirnov test
    - ランダムに選択した2領域
      - [x] $X \in \mathcal{N} (128, 1)$, $N=10$, $h=0.5$
    - 平均が最大と最小の2領域
      - max, min の Event を追加
      - [x] $X \in \mathcal{N} (128, 1)$, $N=10$, $h=0.5$
    - サイズの大きい順に2領域
      - [x] $X \in \mathcal{N} (128, 10)$, $N=10$, $h=5$
  - [ ] naive-FPR と selective-FPR の比較

- [ ] 検出力の評価
  - [x] サイズの大きい順に2領域
  - [ ] 正規分布の真の平均の差が(1, $\ldots$, 10)である系列を生成し, $h = \sigma, 2\sigma, 3\sigma, \sigma = 1$で1000回実験
  - [ ] 棄却率の評価
  
