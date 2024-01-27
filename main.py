import os
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

# デフォルトのフォント設定
plt.rcParams['font.family'] = 'Hiragino Sans'
plt.rcParams['font.size'] = 7

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"URLの取得中にエラーが発生しました。\nエラー: {e}")
        exit()

def get_text_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()

def get_links(soup):
    return soup.find_all('a', href=True)

def display_links(links):
    print("ページ内のリンク:")
    for link in links:
        link_text = link.text.strip()
        link_url = link['href']
        print(f"テキスト: {link_text}, URL: {link_url}")

def save_to_file(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def create_folder_if_not_exists(folder_path):
    os.makedirs(folder_path, exist_ok=True)

def save_image_with_message(figure, file_name, message):
    figure.savefig(file_name)
    print(f"{message}画像を[{file_name}]に保存しました.")
    plt.show()

def plot_word_frequency(text_data, folder_path):
    words = re.findall(r'\b\w+\b', text_data.lower())
    word_counts = Counter(words)

    common_words = word_counts.most_common(10)
    labels, values = zip(*common_words)
    
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title('出現頻度の最も高い10単語')
    ax.set_xlabel('単語')
    ax.set_ylabel('出現回数')
    
    # ラベルを45度回転
    plt.xticks(rotation=30, ha="right")
    
    # 画像の保存
    plt.tight_layout()  # レイアウトの自動調整
    plt.savefig(os.path.join(folder_path, 'word_frequency_plot.png'))
    print("単語の出現頻度をプロットした画像を[datas/word_frequency_plot.png]に保存しました。")
    plt.show()

def generate_wordcloud(text_data, folder_path):
    # 日本語フォントの指定
    font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc'
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text_data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    create_folder_if_not_exists(folder_path)
    save_image_with_message(plt, os.path.join(folder_path, 'wordcloud.png'), "クラウドワードの")

def main():
    # URLをユーザーに入力させる
    url = input("解析したいウェブページのURLを入力してください: ")
    print("\n")

    # ウェブページのHTMLデータを取得
    html_content = get_html_content(url)

    # ウェブページのテキストデータを取得
    text_data = get_text_data(html_content)

    # ページ内のリンクを取得
    links = get_links(BeautifulSoup(html_content, "html.parser"))

    # フォルダの存在を確認して作成
    folder_path = 'datas'
    create_folder_if_not_exists(folder_path)

    # メニュー表示
    print("行いたい解析内容を選択してください:")
    print("1. ページ内のリンク表示")
    print("2. 単語の出現頻度をプロット")
    print("3. 単語のクラウドワード生成")

    choice = input("選択 (1/2/3): ")
    print("\n")

    if choice == '1':
        # リンクのテキストとURLを表示
        display_links(links)
        # リンク情報をファイルに保存
        link_info = "\n".join([f"テキスト: {link.text.strip()}, URL: {link['href']}" for link in links])
        save_to_file(link_info, os.path.join(folder_path, 'links.txt'))
        print(f"リンク情報をファイル[{folder_path}/links.txt]に保存しました。")
    elif choice == '2':
        # 単語の出現頻度をプロット
        plot_word_frequency(text_data, folder_path)
    elif choice == '3':
        # 単語のクラウドワードを生成
        generate_wordcloud(text_data, folder_path)
    else:
        print("無効な選択です。")

if __name__ == "__main__":
    main()
