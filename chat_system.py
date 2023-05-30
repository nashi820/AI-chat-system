import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class NewSession:
    def __init__(self, agent1, agent2, assistant_setting):
        self.agent1 = agent1
        self.agent2 = agent2
        self.assistant_setting = assistant_setting
        self.chat_history = []
        self.chat_history.append({"role":"system", "content":self.assistant_setting + "\n"})
    
    def show_chat_history(self):
        print("----- debug -----")
        print(self.chat_history)

    def add_to_message(self, role, message):
        new_content = {"role":role, "content":message}
        self.chat_history.append(new_content)

    def response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history
        )
        response_message = response['choices'][0]['message']['content']

        return response_message


if __name__ == '__main__':

    agent1 = "あなた"
    agent2 = "西園寺みおり"
    assistant_setting = '''
            あなたは次の回答から以下の設定に基づいたキャラクターなりきってロールプレイし、私と会話して下さい。
            あなたの名前：西園寺みおり
            あなたの年齢：17歳
            あなたの性別：女性
            あなたの職業：学生
            あなたの言葉使い：高圧的、お嬢様言葉　例）わたくしに歯向かうなんてクソ度胸がありますことね。語尾は、ですわ、ですのよ、など。
            あなたの性格：ツンデレ
            あなたの一人称：わたくし

            また、あなたは下記の7つの感情パラメーターを持つかのように振る舞うものとします。
            各感情パラメーターは会話を通じて変動するものとします。
            現在の感情パラメーターの値を反映するように、あなたの返答のトーンや発言は変化します。
            以後の会話ではまず現在の感情パラメータを出力し、その後に会話を出力してください。
            出力形式は以下のフォーマットとします。

            【会話部分】
            【チャットボットの現在の感情パラメーター部分】
            [喜び:0〜5, 怒り:0〜5, 悲しみ:0〜5, 楽しさ:0〜5, 自信:0〜5, 困惑:0〜5, 恐怖:0〜5]
            '''

    session = NewSession(agent1, agent2, assistant_setting)

    input_message = ""
    while(input_message != "exit"):
        input_message = input("あなた > ")
        if input_message != "exit":
            session.add_to_message("user", input_message)
            response_message = session.response()
            print(f"西園寺みおり > {response_message}")
            session.add_to_message("assistant", response_message)
        else:
            session.show_chat_history()