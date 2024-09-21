#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Saturday Sep 21 11:32:19 2024
@author: Sangwon Chae

"""
import csv
import datetime
import os
import queue
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading

class KakaoAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("카카오톡 메시지 분석기")
        master.geometry("600x600")

        self.file_path = tk.StringVar()
        self.target_user = tk.StringVar()
        self.search_var = tk.StringVar()
        self.users = []
        self.gui_queue = queue.Queue()

        # 파일 선택
        tk.Label(master, text="CSV 파일:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(master, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(master, text="찾아보기", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        # 사용자 검색
        tk.Label(master, text="사용자 검색:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.search_entry = tk.Entry(master, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)
        self.search_entry.bind('<KeyRelease>', self.search_users)

        # 사용자 선택
        tk.Label(master, text="분석할 사용자:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.user_combo = ttk.Combobox(master, textvariable=self.target_user, width=47, state="readonly")
        self.user_combo.grid(row=2, column=1, padx=5, pady=5)

        # 사용자 정의 프롬프트 입력
        tk.Label(master, text="사용자 정의 프롬프트:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.prompt_text = tk.Text(master, height=5, width=50)
        self.prompt_text.grid(row=3, column=1, padx=5, pady=5)

        # 분석 버튼
        tk.Button(master, text="분석 시작", command=self.start_analysis).grid(row=4, column=1, pady=10)

        # 결과 표시
        self.result_text = tk.Text(master, height=15, width=70)
        self.result_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # 스크롤바
        scrollbar = tk.Scrollbar(master, command=self.result_text.yview)
        scrollbar.grid(row=5, column=3, sticky='nsew')
        self.result_text['yscrollcommand'] = scrollbar.set

        # OpenAI API 키 읽기
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        if not self.OPENAI_API_KEY:
            messagebox.showerror("오류", "OpenAI API 키가 설정되지 않았습니다.")
            master.destroy()

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.file_path.set(filename)
            self.load_users()

    def load_users(self):
        try:
            with open(self.file_path.get(), 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # 헤더 스킵
                self.users = list(set(row[1] for row in reader if len(row) > 1))
            self.user_combo['values'] = sorted(self.users)
        except Exception as e:
            messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")

    def search_users(self, event):
        search_term = self.search_var.get().lower()
        filtered_users = [user for user in self.users if search_term in user.lower()]
        self.user_combo['values'] = sorted(filtered_users)

    def start_analysis(self):
        if not self.file_path.get() or not self.target_user.get():
            messagebox.showerror("오류", "파일과 사용자를 선택해주세요.")
            return

        custom_prompt = self.prompt_text.get('1.0', tk.END).strip()
        if not custom_prompt:
            messagebox.showerror("오류", "사용자 정의 프롬프트를 입력해주세요.")
            return

        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "분석 중...\n")

        # 큐 처리 시작
        self.master.after(100, self.process_queue)

        # 분석을 별도의 스레드에서 실행
        threading.Thread(target=self.run_analysis, args=(custom_prompt,), daemon=True).start()

    def run_analysis(self, custom_prompt):
        try:
            messages = self.read_csv(self.file_path.get())
            filtered_messages = self.filter_messages(messages, self.target_user.get())
            self.summarize_and_analyze(filtered_messages, custom_prompt)
        except Exception as e:
            messagebox.showerror("오류", f"분석 중 오류가 발생했습니다: {str(e)}")

    def read_csv(self, file_path):
        messages = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 헤더 스킵
            for row in reader:
                if len(row) == 3:
                    date_str, user, content = row
                    try:
                        # 여러 날짜 형식 시도
                        date_formats = ['%Y-%m-%d %H:%M:%S', '%Y.%m.%d %H:%M', '%Y-%m-%d %H:%M']
                        for date_format in date_formats:
                            try:
                                date = datetime.datetime.strptime(date_str, date_format)
                                break
                            except ValueError:
                                continue
                        else:
                            raise ValueError(f"지원되지 않는 날짜 형식: {date_str}")

                        messages.append({
                            'date': date,
                            'user': user,
                            'content': content
                        })
                    except ValueError as e:
                        print(f"날짜 파싱 오류 (무시됨): {e}")
        return messages

    def filter_messages(self, messages, target_user):
        filtered = []
        for i, msg in enumerate(messages):
            if msg['user'] == target_user:
                start = max(0, i - 5)
                end = min(len(messages), i + 6)
                context = messages[start:end]
                filtered.append({'message': msg, 'context': context})
        return filtered

    def summarize_and_analyze(self, filtered_messages, custom_prompt):
        client = OpenAI(api_key=self.OPENAI_API_KEY)

        for item in filtered_messages:
            main_message = item['message']
            context = item['context']

            # 사용자 정의 프롬프트 사용
            prompt = custom_prompt + "\n\n"
            for msg in context:
                prompt += f"{msg['date']}: {msg['user']}: {msg['content']}\n"

            try:
                response = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[
                        {"role": "system", "content": "당신은 대화 내용을 심도있게 분석하고 요약하는 전문가입니다."},
                        {"role": "user", "content": prompt}
                    ]
                )

                summary = {
                    'date': main_message['date'],
                    'summary': response.choices[0].message.content
                }

                # 결과를 큐에 추가
                self.gui_queue.put(summary)
            except Exception as e:
                self.gui_queue.put({'date': main_message['date'], 'summary': f"오류 발생: {str(e)}"})

    def process_queue(self):
        try:
            while True:
                summary = self.gui_queue.get_nowait()
                self.result_text.insert(tk.END, f"\n날짜: {summary['date']}\n")
                self.result_text.insert(tk.END, summary['summary'])
                self.result_text.insert(tk.END, "\n" + "-"*50 + "\n")
                self.result_text.see(tk.END)  # 스크롤을 최신 내용으로 이동
        except queue.Empty:
            pass
        # 큐를 지속적으로 확인
        self.master.after(100, self.process_queue)

def main():
    root = tk.Tk()
    KakaoAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
