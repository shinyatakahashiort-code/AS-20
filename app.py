import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import json
import os
from datetime import datetime

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Hiragino Sans', 'Yu Gothic', 'Meiryo']
matplotlib.rcParams['axes.unicode_minus'] = False

# ページ設定
st.set_page_config(
    page_title="視覚のQOL調査 AS-20",
    page_icon="👁️",
    layout="wide"
)

# データ保存用ディレクトリ
DATA_DIR = "survey_data"
os.makedirs(DATA_DIR, exist_ok=True)

# AS-20アンケート質問項目
QUESTIONS = [
    "1. 私の目が人にどう見られるかが気になる",
    "2. 何も言われなくても、人が私の目のことを気にしているように感じる",
    "3. 私の目のせいで、人に見られていると不快に感じる",
    "4. 自分の目のせいで、私を見ている人が、何を考えているのだろうと考えてしまう",
    "5. 自分の目のせいで、人は私に機会を与えてくれない",
    "6. 私は自分の目を気にしている",
    "7. 自分の目のせいで、人は私を見るのを避ける",
    "8. 自分の目のせいで、他の人より劣っていると感じる",
    "9. 自分の目のせいで、人は私に対して違う反応をする",
    "10. 自分の目のせいで、初対面の人との交流が難しいと感じる",
    "11. ものが良く見えるように、片方の目を隠したり閉じたりすることがある",
    "12. 自分の目のせいで、読むのを避けてしまう",
    "13. 自分の目のせいで、集中できないので、物事を中断している",
    "14. 奥行きの感覚に問題があると思う",
    "15. 目が疲れる",
    "16. 自分の目の調子のせいで、読むことに支障をきたしている",
    "17. 自分の目が原因で、ストレスを感じる",
    "18. 自分の目が心配だ",
    "19. 自分の目が気になって、趣味を楽しめない",
    "20. 自分の目のせいで、読むときに頻繁に休憩する必要がある"
]

# リッカート尺度の選択肢
LIKERT_OPTIONS = [
    "全くない",
    "まれにしかない",
    "時々ある",
    "よくある",
    "いつもある"
]

# スコアマッピング
SCORE_MAP = {
    "全くない": 100,
    "まれにしかない": 75,
    "時々ある": 50,
    "よくある": 25,
    "いつもある": 0
}

# サブスケール定義
PSYCHOSOCIAL_ITEMS = list(range(0, 10))  # 質問1-10（インデックス0-9）
FUNCTIONAL_ITEMS = list(range(10, 20))   # 質問11-20（インデックス10-19）

def save_response(name, patient_id, responses):
    """回答を保存する関数"""
    scores = [SCORE_MAP[r] for r in responses]
    total_score = sum(scores)
    psychosocial_score = sum(scores[i] for i in PSYCHOSOCIAL_ITEMS)
    functional_score = sum(scores[i] for i in FUNCTIONAL_ITEMS)
    
    # 平均点を計算
    total_avg = total_score / 20
    psychosocial_avg = psychosocial_score / 10
    functional_avg = functional_score / 10
    
    data = {
        "name": name,
        "patient_id": patient_id,
        "timestamp": datetime.now().isoformat(),
        "responses": responses,
        "scores": scores,
        "total_score": total_score,
        "psychosocial_score": psychosocial_score,
        "functional_score": functional_score,
        "total_avg": total_avg,
        "psychosocial_avg": psychosocial_avg,
        "functional_avg": functional_avg
    }
    
    # JSON形式で保存
    filename = f"{DATA_DIR}/{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data

def create_visualization(data):
    """結果のグラフを作成する関数"""
    fig = plt.figure(figsize=(18, 10))
    
    # グリッドレイアウト: 上段に2つのグラフ
    gs = fig.add_gridspec(1, 2, width_ratios=[2, 1], hspace=0.3, wspace=0.3)
    
    # 1. 項目ごとのスコア棒グラフ（左側）
    ax1 = fig.add_subplot(gs[0, 0])
    questions_short = [f"Q{i+1}" for i in range(20)]
    colors = ['#2ECC71' if score == 100 else '#95E1D3' if score == 75 else '#FFD93D' if score == 50 else '#FF9A76' if score == 25 else '#FF6B6B' for score in data['scores']]
    bars = ax1.barh(questions_short, data['scores'], color=colors, edgecolor='black', linewidth=0.8)
    ax1.set_xlabel('Score (out of 100)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Question Items', fontsize=13, fontweight='bold')
    ax1.set_title('Scores for Each Item (100 points maximum per item)', fontsize=16, fontweight='bold', pad=15)
    ax1.set_xlim(0, 110)
    ax1.invert_yaxis()
    
    
    # スコアをバーに表示
    for bar, score in zip(bars, data['scores']):
        width = bar.get_width()
        ax1.text(width + 2, bar.get_y() + bar.get_height()/2, f'{int(score)}',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    # 2. 平均点の比較（全体・心理面・機能面）（右側）
    ax2 = fig.add_subplot(gs[0, 1])
    categories = ['Overall\n(Q1-20)', 'Psychosocial\n(Q1-10)', 'Functional\n(Q11-20)']
    avg_scores = [data['total_avg'], data['psychosocial_avg'], data['functional_avg']]
    colors_bar = ['#9B59B6', '#E74C3C', '#3498DB']
    
    bars2 = ax2.bar(categories, avg_scores, color=colors_bar, 
                    edgecolor='black', linewidth=1.5, alpha=0.85, width=0.6)
    ax2.set_ylabel('Average Score (out of 100)', fontsize=12, fontweight='bold')
    ax2.set_title('Average Score by Category', fontsize=15, fontweight='bold', pad=12)
    ax2.set_ylim(0, 110)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 基準線
    ax2.axhline(y=75, color='green', linestyle=':', linewidth=2, alpha=0.5)
    ax2.axhline(y=50, color='orange', linestyle=':', linewidth=2, alpha=0.5)
    ax2.axhline(y=25, color='red', linestyle=':', linewidth=2, alpha=0.5)
    
    # 平均点をバーの上に表示
    for bar, score in zip(bars2, avg_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 3,
                f'{score:.1f}',
                ha='center', va='bottom', fontsize=13, fontweight='bold')
    
    # 達成率も表示（バー内部）
    for i, (bar, score) in enumerate(zip(bars2, avg_scores)):
        ax2.text(bar.get_x() + bar.get_width()/2., score/2,
                f'{score:.1f}%',
                ha='center', va='center', fontsize=11, fontweight='bold', 
                color='white')
    
    plt.tight_layout()
    return fig

# アプリケーションのメイン部分
st.title("📋 視覚のQOL調査 AS-20")

st.markdown("""
本アンケートは斜視や斜視の疑いのある方への簡易的な国際的に有用な質問票です。
斜視が日常生活にどのような影響を与えるのか調査する目的で行っています。

**全部で20項目あります。** 各項目ご自身のお気持ちをよく表している項目を選択してください。
""")

st.divider()

# 患者情報入力
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("氏名 *", placeholder="お名前を入力してください")
with col2:
    patient_id = st.text_input("患者ID *", placeholder="患者IDを入力してください")

st.divider()

st.subheader("📝 アンケート質問")
st.caption("*すべての質問にお答えください*")

# 20個の質問を表示
responses = []
for i, question in enumerate(QUESTIONS):
    response = st.radio(
        question,
        options=LIKERT_OPTIONS,
        index=None,
        key=f"q{i}",
        horizontal=True
    )
    responses.append(response)

st.divider()

# 送信ボタン
if st.button("✅ 回答を送信してスコアを表示", type="primary", use_container_width=True):
    if not name or not patient_id:
        st.error("❌ **エラー:** 氏名とIDを入力してください。")
    elif None in responses:
        st.error("❌ **エラー:** すべての質問に回答してください。")
    else:
        # データ保存
        data = save_response(name, patient_id, responses)
        
        # 結果表示
        st.success("✅ 回答を送信しました！")
        
        st.divider()
        st.header("📊 結果")
        
        # QOL評価レベルの判定
        if data['total_avg'] >= 75:
            qol_level = "良好（軽度の影響）"
            level_color = "🟢"
        elif data['total_avg'] >= 50:
            qol_level = "中程度（中程度の影響）"
            level_color = "🟡"
        elif data['total_avg'] >= 25:
            qol_level = "低下（顕著な影響）"
            level_color = "🟠"
        else:
            qol_level = "著しい低下（重度の影響）"
            level_color = "🔴"
        
        # サマリー表示
        st.subheader(f"総合評価 {level_color}")
        st.markdown(f"**QOL レベル:** {qol_level}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("全体平均点", f"{data['total_avg']:.1f}点")
        with col2:
            st.metric("心理社会面平均点", f"{data['psychosocial_avg']:.1f}点")
        with col3:
            st.metric("機能面平均点", f"{data['functional_avg']:.1f}点")
        
        # グラフ表示
        fig = create_visualization(data)
        st.pyplot(fig)
        
        # 質問内容の表示（Streamlitの表として追加）
        st.subheader("📋 質問項目一覧")
        
        # 質問内容をDataFrameで表示
        questions_df = pd.DataFrame({
            'Q1-Q10 (心理社会面)': [
                "Q1: 私の目が人にどう見られるかが気になる",
                "Q2: 何も言われなくても、人が私の目のことを気にしているように感じる",
                "Q3: 私の目のせいで、人に見られていると不快に感じる",
                "Q4: 自分の目のせいで、私を見ている人が、何を考えているのだろうと考えてしまう",
                "Q5: 自分の目のせいで、人は私に機会を与えてくれない",
                "Q6: 私は自分の目を気にしている",
                "Q7: 自分の目のせいで、人は私を見るのを避ける",
                "Q8: 自分の目のせいで、他の人より劣っていると感じる",
                "Q9: 自分の目のせいで、人は私に対して違う反応をする",
                "Q10: 自分の目のせいで、初対面の人との交流が難しいと感じる"
            ],
            'Q11-Q20 (機能面)': [
                "Q11: ものが良く見えるように、片方の目を隠したり閉じたりすることがある",
                "Q12: 自分の目のせいで、読むのを避けてしまう",
                "Q13: 自分の目のせいで、集中できないので、物事を中断している",
                "Q14: 奥行きの感覚に問題があると思う",
                "Q15: 目が疲れる",
                "Q16: 自分の目の調子のせいで、読むことに支障をきたしている",
                "Q17: 自分の目が原因で、ストレスを感じる",
                "Q18: 自分の目が心配だ",
                "Q19: 自分の目が気になって、趣味を楽しめない",
                "Q20: 自分の目のせいで、読むときに頻繁に休憩する必要がある"
            ]
        })
        
        st.dataframe(questions_df, use_container_width=True, hide_index=True)
        
        # 解釈ガイド
        with st.expander("📖 結果の解釈ガイド"):
            st.markdown("""
            ### 平均点の意味
            - **高得点（75-100点）**: 視覚の問題が日常生活に与える影響が少なく、QOLは良好です
            - **中程度（50-74点）**: 中程度の影響があり、生活の質にある程度の制約が見られます
            - **低得点（25-49点）**: 顕著な影響があり、日常生活に大きな制約があります
            - **著しい低下（0-24点）**: 重度の影響があり、QOLが著しく低下しています
            
            **注意:** このスコアは自己評価に基づくものであり、医療専門家による診断の代わりにはなりません。
            結果については主治医にご相談ください。
            """)

st.divider()
st.caption("© 2025 視覚のQOL調査 AS-20 | すべての回答は自動的に保存されます")
