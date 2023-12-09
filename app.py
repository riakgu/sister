import threading
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# Algoritma LCS Dynamic Programming
def lcs_dp(X, Y, m, n):
    LCS = [[0] * (n+1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j- 1]:
                LCS[i][j] = 1 + LCS[i - 1][j - 1]
            else:
                LCS[i][j] = max(LCS[i - 1][j], LCS[i][j - 1])

    return LCS[m][n]

# Fungsi untuk Compare Text
def compare_texts(user_text, file_text, file_name, comparisons):
    
    lcs_length = lcs_dp(user_text, file_text, len(user_text), len(file_text))

    similarity = (lcs_length / max(len(user_text), len(file_text))) * 100

    comparisons.append({
        'file_name': file_name,
        'similarity': similarity
    })


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_text = request.form['text1'].lower().split()
    comparisons = []
    threads = []

    for i in range(1, 11):
        with open(f'files/{i}.txt', 'r') as file:
            file_text = file.read().lower().split()

        # Membuat thread untuk setiap file
        thread = threading.Thread(target=compare_texts, args=(user_text, file_text, f'{i}.txt', comparisons))
        threads.append(thread)
        thread.start()

    # Menunggu semua thread selesai
    for thread in threads:
        thread.join()

    return render_template('result.html', comparisons=comparisons)


if __name__ == '__main__':
    app.run()
