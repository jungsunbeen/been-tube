# 다음 세션 프롬프트 (복사해서 붙여넣기)

~/lofi 프로젝트 이어서 진행. 목표: Suno로 만든 로파이 곡들을 1시간짜리 유튜브 영상으로 만들기.

## 현재 상태
- Suno 곡 2개가 ~/lofi/suno/에 있음: "Paper Sun.mp3", "Paper Moon.mp3" (확인 완료)
- Python 환경: ~/lofi/.venv (Python 3.12, uv로 생성. uv는 ~/.local/bin/uv)
  - 설치됨: numpy, pedalboard(mp3 읽기/쓰기 가능), tinysoundfont, demucs, basic-pitch
- yt-dlp: ~/bin/yt-dlp
- ffmpeg: 미설치 (Homebrew도 없음 — evermeet.cx 정적 바이너리나 uv/pip 대안 검토)
- 참고 분석 자료: ggg. 채널 원곡 분석 완료
  - 1시간 영상 공식: 같은 곡을 조성(±1~2반음)·템포·필터로 변주하며 순환
  - 레시피 상세: ~/lofi/compose2.py 주석 참고

## 해야 할 일
1. 1시간 믹스 스크립트 작성 (.venv/bin/python 사용):
   - 각 곡의 변주 생성: pedalboard PitchShift ±1~2 반음, 살짝 어둡거나 밝은 필터, (선택) 미세 템포 변화
   - 곡 순서: A → B → A변주 → B변주 ... 식으로 교차, 2~4초 크로스페이드로 이어붙여 정확히 60분
   - 결과: ~/lofi/mix-1hour.wav (또는 mp3)
3. 커버 이미지 1장 준비 (사용자에게 요청하거나 단색+텍스트로 생성)
4. ffmpeg 설치 후: 이미지 + 오디오 → 유튜브용 mp4
   (ffmpeg -loop 1 -i cover.jpg -i mix.mp3 -c:v libx264 -tune stillimage -c:a aac -shortest out.mp4)
5. 업로드는 사용자가 YouTube Studio에서 수동

## 주의
- Suno 무료 플랜은 상업적 이용(수익화) 불가 — 수익화하려면 유료 플랜 필요하다고 사용자에게 상기시킬 것
- ggg. 원곡 오디오 파일들(ggg-*.wav/m4a)은 분석용 — 절대 믹스에 포함하거나 업로드 금지 (저작권)
- 디스크 용량: ~/lofi에 분석용 대용량 파일 많음 (ggg wav 310MB 등) — 필요하면 정리
