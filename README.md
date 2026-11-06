# been-tube

**"한 영상 = 한 도시의 한 장면"** — 세계 도시의 특정 시간대·날씨를 lofi jazz 1시간 믹스로 만드는 유튜브 채널 제작 파이프라인.

Suno로 생성한 소스곡 폴더를 넣으면 키·BPM 실측 QC → 플레이리스트 큐레이션 → 믹스 렌더 → mp4 인코딩 → 백업 → 업로드용 완료 문서까지 Claude Code 스킬 하나로 진행한다. 사람은 곡 생성과 큐레이션 승인만 맡는다.

완성: Florence, London, Paris, Prague, Berlin

## 왜 이렇게 만들었나

경쟁 채널 4곳(ggg., fo., 야채상회, あつ森)의 믹스 오디오를 직접 분석해 포맷을 정했다. 분석 스크립트와 결과는 `scripts/analyze_*.py`, `docs/Analyze/`에 있다.

| 채널 | 구조 |
|---|---|
| ggg. | 30분 세트(9~10곡) × 2회, 키·템포 변화 |
| fo. | 69분 세트 × 3회, C장조권 ~64 BPM 고정 |
| 야채상회 | 63분 세트 × 2회, 키·템포 자유 |
| あつ森 | 90분 세트 × 2회, 빗소리 레이어 전곡 일정 |

반복 주기 자기유사도 분석으로 확인한 공통점: **장시간을 유니크 오디오로 채우는 채널은 없다. 세트 하나를 2~3회 통반복한다.** 이 결론에 따라 `build_mix.py`는 곡을 변주하지 않고 ~10곡 → ~32분 세트 → 2회 반복으로 1시간을 만든다.

설계에서 내린 주요 결정:

- **앰비언스는 Suno 프롬프트에서 뺀다.** 곡마다 다른 빗소리가 생성되면 트랙 경계가 드러나고 키·BPM 실측도 오염된다. 후반작업에서 세트 전체에 한 레이어로 얹는다.
- **생성 결과는 반드시 실측한다.** 1일차 실측에서 Suno는 BPM은 8곡 모두 ±3 이내로 따랐지만, 키는 8곡 중 5곡만 지켰다. 어긋난 곡은 전부 샤프·플랫이 많은 키였다. 그래서 도시 키를 조표가 단순한 키로 바꿨다(Tokyo: F#m → Em + G장조).
- **QC 판정 기준을 수치로 고정한다.** 목표 키 대비 ±1~2반음은 time_stretch로 보정하고, ±3반음 이상은 드럼 트랜지언트가 번지므로 재생성한다.

전체 설계 근거: [`docs/project.md`](docs/project.md), 장르 확장: [`docs/genre-palette.md`](docs/genre-palette.md)

## 파이프라인

```
[사람] Suno 생성(곡 제목 지정) → audio/suno/{city}/
[스킬] ① 소스 확인
       ② 키·BPM 실측 QC (librosa 크로마 + Krumhansl 키 프로파일)
       ③ 소스곡 Google Drive 백업
       ④ 플레이리스트 큐레이션 ── curator 3인 패널 제안 → [사람] 승인
       ⑤ 세트 ×2 렌더 (build_mix.py) + 유튜브 타임스탬프 출력
       ⑥ 썸네일 + wav → H.264/AAC mp4
       ⑦ 최종본 백업 + 바이트 크기 대조 검증
       ⑧ 완료 문서 (트랙리스트, 유튜브 설명란, 업로드 체크리스트, 예비곡)
[사람] 유튜브 업로드
```

### Claude Code 스킬 · 에이전트

| 파일 | 역할 |
|---|---|
| [`.claude/skills/lofi-city-mix/SKILL.md`](.claude/skills/lofi-city-mix/SKILL.md) | 위 ①~⑧ 절차. "{도시} 곡 넣었어"로 발동하고, 도시 슬러그만 바뀌며 절차는 같다 |
| [`.claude/agents/curator.md`](.claude/agents/curator.md) | 실측 데이터만으로 세트리스트 1안을 제안하는 큐레이터. ④에서 서로 다른 렌즈로 3개를 병렬 호출한다 |

큐레이션 순서 원칙 7개(밝은 키로 진입, 템포 두 번 출렁임, 인접 트랙 같은 조성 금지 등)는 curator의 하드 제약이다. curator는 제출 전에 모든 인접 쌍과 마지막 곡→첫 곡 랩어라운드의 반음 간격을 직접 세어 검증한다.

안전장치:
- ④ 큐레이션은 사용자가 승인하기 전에는 다음 단계로 넘어가지 않는다.
- 로컬 산출물은 업로드 바이트 검증을 통과하고 사용자가 확인했을 때만 삭제한다.
- 곡의 피치·멜로디·템포는 바꾸지 않는다. ±2반음 이내 QC 보정만 예외다.

## 스크립트

| 분류 | 파일 | 하는 일 |
|---|---|---|
| 제작 | `build_mix.py` | 무음 제거, 중앙값 RMS 음량 통일, 등파워 3초 크로스페이드, 세트 2회 반복, 피크 리미터. 트랙 순서는 파일 안 `PROJECTS`에 도시별로 정의 |
| 경쟁 분석 | `analyze_mix.py` | 장시간 믹스의 BPM·조성 타임라인과 반복 주기 자동 탐지 |
| | `refine_offset.py` | 반복 주기 후보를 초 단위로 보정한 뒤 통반복 여부 재검증 |
| | `analyze_sources.py` | 세트 안 트랙이 서로 다른 곡인지, 한 곡의 피치·템포 변주인지 판별 (12 조옮김 × 템포 비율 정렬) |
| | `analyze_chords.py`, `analyze_timbre.py`, `verify_matcha.py` | 코드 진행 추정, 음색 진단, 분석 결과 독립 검증 |
| 전사 | `separate.py`, `transcribe.py` | Demucs 스템 분리 → basic-pitch MIDI 전사 → 작곡 문법 리포트 |
| 작곡 실험 | `compose.py`, `compose2.py`, `compose_fo.py`, `check_chords.py` | 분석에서 뽑은 문법으로 직접 작곡(tinysoundfont + pedalboard)하고 렌더 결과의 코드 검증 |

## 실행

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install librosa numpy scipy pedalboard imageio-ffmpeg
# 전사·작곡 실험까지 쓸 때
pip install demucs torch torchaudio basic-pitch tinysoundfont
```

- ffmpeg는 따로 설치하지 않고 `imageio-ffmpeg`에 들어 있는 바이너리를 쓴다.
- 백업 단계는 `rclone`에 `gdrive:` 리모트가 설정되어 있어야 한다.
- `audio/`는 용량 때문에 `.gitignore`에 들어 있다. 소스곡은 `audio/suno/{city}/`에 둔다.

믹스만 직접 렌더할 때:

```bash
python scripts/build_mix.py florence   # → audio/output/florence-1hour.wav
```

## 디렉토리

```
.claude/        스킬, curator 에이전트
docs/
  project.md        채널 설계 문서
  genre-palette.md  장르 확장 설계
  Analyze/          경쟁 채널 분석 결과
  prompts/          도시별 Suno 프롬프트, complete/ 에 완료 문서
scripts/        분석·제작·작곡 스크립트
image/          썸네일
models/         작곡 실험용 사운드폰트 (GeneralUser GS)
```

## 알려진 한계

- SKILL.md의 작업 디렉토리와 Google Drive 폴더 ID가 작성 당시 머신 기준 고정값이다.
- 키·BPM 실측 코드가 SKILL.md 안에 인라인으로 들어 있고, 테스트가 없다.
- Suno 무료 플랜으로 생성한 곡은 상업 이용이 불가해 수익 창출을 끈 상태로 운영한다.
