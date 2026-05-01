from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="저는 mock-interview-ai 프로젝트에서 Redis를 캐싱 용도로 활용했습니다. 동일한 채용공고 URL로 반복 요청이 들어올 때마다 크롤링과 GPT 호출이 발생해서 응답 시간이 길어지는 문제가 있었습니다. 이를 해결하기 위해 공고 크롤링 결과를 Redis에 1시간 동안 캐싱했고, 두 번째 요청부터는 캐시에서 바로 반환되어 응답 속도가 크게 개선됐습니다."
)

response.stream_to_file("test_answer.mp3")
print("완료: test_answer.mp3")