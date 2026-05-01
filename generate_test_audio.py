from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="안녕하세요. 저는 Python과 FastAPI를 활용한 백엔드 개발 경험이 있습니다. Redis를 이용한 캐싱 시스템을 구현했으며, Docker 환경에서 배포한 경험도 있습니다. 해당 프로젝트에서 응답 속도를 30퍼센트 개선했습니다."
)

response.stream_to_file("test_answer.mp3")
print("완료: test_answer.mp3")