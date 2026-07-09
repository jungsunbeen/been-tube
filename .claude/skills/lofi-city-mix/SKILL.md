---
name: lofi-city-mix
description: >
  도시 시리즈 lofi 1시간 믹스를 Suno 소스곡 폴더에서 업로드용 mp4까지 만드는 전체 파이프라인.
  Use when the user says "{도시} 곡 넣었어", "{도시} 곡 다 넣었어", "플로렌스 곡 넣었어",
  "런던 믹스 만들어줘", "{도시} 1시간 믹스 만들어", "{도시} 영상 만들어줘",
  or has dropped Suno mp3s into audio/suno/{city}/ and wants the full
  실측 → gdrive 백업 → 플레이리스트 큐레이션(미사용곡 기록) → 합치기 → 이미지+mp4 → 최종 백업 → 완료문서 flow.
  도시명(florence/london/paris/...)만 바뀌고 절차는 동일하다.
---

# lofi-city-mix: 도시 lofi 믹스 파이프라인

"한 영상 = 한 도시의 한 장면" lofi jazz 1시간 믹스를, Suno로 생성한 소스곡들에서
업로드 가능한 mp4까지 만든다. ggg. 검증 공식: **서로 다른 곡 ~10개 → ~32분 세트 → 2회 반복**.
곡 자체는 변주하지 않고 믹싱 손질(무음 제거·음량 통일·등파워 크로스페이드)만 한다.

설계 근거는 `docs/project.md`, 레퍼런스 완성본은
`docs/prompts/complete/florence-complete.md`. 작업 디렉토리는 `/Users/jungsunbeen/lofi`.

## 트리거

사용자가 "{도시} 곡 넣었어" 류로 말하면 발동. `{도시}`(영문 소문자 슬러그, 예: `florence`,
`london`)를 확정하고 `audio/suno/{city}/` 에 mp3가 있는지부터 확인한다. 없으면 도시명/경로를 되묻는다.

## 환경 (이 머신 고정값)

- ffmpeg: 별도 설치 없음. `.venv`의 imageio-ffmpeg 바이너리를 쓴다.
  `FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")`
- Google Drive: `rclone`(`~/.local/bin/rclone`)에 `gdrive:` 리모트가 설정돼 있음.
  - 소스곡 백업 폴더 `suno`  = folder-id `143KPGQS8wRkUfuxJRFQ9FG-6-2cGuFt1`
  - 최종본 백업 폴더 `output` = folder-id `1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R`
  - 폴더 구조가 바뀌면 `rclone lsf gdrive:` 또는 Google Drive MCP `search_files`로 ID를 다시 찾는다.
  - 도시별 하위폴더(`output/{city}/`, `suno/{city}/`)에 넣는다. rclone은 목적지 경로에
    하위폴더가 없으면 자동 생성한다.

## 단계

### ① 소스 확인
`ls -la audio/suno/{city}/` 로 mp3 개수·이름 확인. 보통 10~16개(변형 쌍 포함).

### ② 키/BPM 실측 (QC)
곡마다 조성과 BPM을 측정한다. 아래를 그대로 실행:

```bash
cd /Users/jungsunbeen/lofi
python3 - "audio/suno/{city}" <<'PY'
import sys, glob, os, numpy as np, librosa
KS_MAJ=np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
KS_MIN=np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
N=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
for f in sorted(glob.glob(sys.argv[1]+"/*.mp3")):
    y,sr=librosa.load(f,sr=22050,mono=True)
    ch=librosa.feature.chroma_cqt(y=y,sr=sr).mean(axis=1)
    best,bs=None,-9
    for r in range(12):
        for prof,lab in ((KS_MAJ,"장조"),(KS_MIN,"단조")):
            s=np.corrcoef(np.roll(prof,r),ch)[0,1]
            if s>bs: bs,best=s,N[r]+lab
    bpm=float(np.atleast_1d(librosa.beat.beat_track(y=y,sr=sr)[0])[0])
    print(f"{os.path.basename(f):34s} {best:7s} {bpm:5.1f} BPM")
PY
```

판정 기준(docs/project.md):
- 도시 목표 키 대비 **±1~2반음**: time_stretch 보정으로 흡수 가능(투명).
- **±3반음 이상**: 재생성 후보로 표시하고 사용자에게 알림(드럼 트랜지언트 번짐).
- BPM은 Suno가 잘 따르므로 보통 문제없음. 키 추정은 근사치이니 애매하면 곡을 들어보게 권한다.

### ③ 소스곡 gdrive 백업 (원본 보존)
재생성을 피하기 위해 소스곡 원본을 먼저 백업한다.

```bash
rclone copy "audio/suno/{city}" "gdrive:{city}" \
  --drive-root-folder-id 143KPGQS8wRkUfuxJRFQ9FG-6-2cGuFt1 \
  --include "*.mp3" -P --stats-one-line
```

### ④ 플레이리스트 큐레이션 ★사용자 승인 필수★
②의 실측을 근거로 **~10곡을 선별·정렬**한다. 순서 원칙(florence 검증):

1. **A장조 등 밝고 따뜻한 키로 진입**(오프너).
2. **템포를 두 번 출렁**이게 배치(예: ↑96 → ↓72 → ↑92) — 단조로움 방지.
3. 중반에 **단조 색채 1곡**으로 명암.
4. **가장 긴 곡을 세트 중심**에 둔다.
5. 후반 **와인드다운** 후, **가장 밝은(고BPM) 곡으로 마감**.
6. **인접 트랙끼리 같은/너무 가까운 조성 금지**(이음새 노출 방지).
7. 변형 쌍 중 하나만 쓰고, **안 쓴 곡·예비곡은 따로 기록**(다음 도시 재활용).

선정 결과(순서 + 곡별 키/BPM + 미사용곡)를 표로 사용자에게 제시하고 **승인을 받는다.**
큐레이션은 이 워크플로우의 창의적 핵심이므로 승인 전에 ⑤로 넘어가지 않는다.

승인되면 `scripts/build_mix.py`의 `PROJECTS` 딕셔너리에 `"{city}"` 키로 순서를 기록한다
(파일명 리스트 + 곡별 `# 키 BPM 역할` 주석). 형식은 기존 `"florence"` 항목을 그대로 따른다.

### ⑤ 합치기 (세트 ×2 렌더)
```bash
python3 scripts/build_mix.py {city}
```
출력: `audio/output/{city}-1hour.wav` (48kHz/16bit 스테레오) + 콘솔에 유튜브 타임스탬프.
스크립트가 자동으로 무음 제거·중앙값 RMS 음량 통일·등파워 3초 크로스페이드·세트 2회 반복·
끝 8초 페이드아웃·피크 리미터를 적용한다. 타임스탬프 출력을 ⑧에 쓰니 보관한다.

### ⑥ 이미지 + mp4 인코딩
썸네일 `image/{city}-16x9.png`(1920×1080)와 wav를 합쳐 H.264+AAC mp4를 만든다.

```bash
cd /Users/jungsunbeen/lofi
FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
"$FFMPEG" -y -loop 1 -framerate 2 -i "image/{city}-16x9.png" -i "audio/output/{city}-1hour.wav" \
  -c:v libx264 -preset medium -tune stillimage -crf 20 -pix_fmt yuv420p \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:a aac -b:a 192k -shortest "audio/output/{city}-1hour.mp4"
```
썸네일이 16:9가 아니면 `image/{city}.png` 원본을 센터 16:9 크롭해 `{city}-16x9.png`를 먼저 만든다.

### ⑦ 최종본 gdrive 백업
```bash
rclone copy "audio/output/{city}-1hour.mp4" "gdrive:{city}" \
  --drive-root-folder-id 1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R -P --stats-one-line
rclone copy "audio/output/{city}-1hour.wav" "gdrive:{city}" \
  --drive-root-folder-id 1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R --stats=15s --stats-one-line
```
큰 wav(수백 MB)는 업로드가 길어질 수 있으니 백그라운드 실행 후 완료 알림에서 검증한다.
검증: 업로드 후 `rclone lsl ... | grep {city}` 의 바이트 크기를 로컬 `stat -f %z` 와 대조해 일치 확인.

**공유 링크 + 로컬 정리 (컴퓨터 용량 절약):**
```bash
rclone link "gdrive:{city}/{city}-1hour.mp4" --drive-root-folder-id 1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R
rclone link "gdrive:{city}/{city}-1hour.wav" --drive-root-folder-id 1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R
```
발급한 링크를 사용자에게 제시하고(완료 문서에도 기록), **사용자가 링크를 확인·승인하면**
로컬 `audio/output/{city}-1hour.wav`/`.mp4`를 삭제한다.
- ⚠️ 삭제는 반드시 **바이트 검증 통과 + 사용자 확인** 두 조건을 모두 충족한 뒤에만.
- ⚠️ 유튜브 업로드는 로컬 mp4가 필요하다 — 유튜브 업로드 전이면 wav만 지우고,
  mp4는 유튜브 업로드를 마친 뒤 지우도록 권한다.

### ⑧ 완료 문서
`docs/prompts/complete/{city}-complete.md`를 생성한다. `florence-complete.md`를 템플릿으로:
- 산출물 경로 표(mp4/wav/썸네일/원본이미지/빌드 명령)
- 최종 트랙 리스트(⑤ 타임스탬프 + 곡별 키/BPM)
- 유튜브 설명란(복붙용: 한 줄 무드 + Track list 타임스탬프 + "Music generated with Suno AI." + 해시태그)
  - Track list 표시명은 소스 파일명 재활용이 아니라 **간단한 새 단어로 새로 짓는다**
    (한두 단어, 테이크 구분 `II`/`(2)` 없이 전부 서로 다른 이름)
- 업로드 체크리스트(제목 형식, 썸네일, **수익 창출 OFF**=Suno 무료 플랜은 비상업적만, "아동용 아님" 설정)
- 미사용 예비 곡 목록

## 완료 보고
사용자에게: 산출물 경로, 총 길이/세트 반복, gdrive 백업·바이트 검증 결과, 재생성 후보(있으면),
미사용 예비곡을 요약한다.

## 주의
- 곡 피치/멜로디/템포를 임의로 바꾸지 않는다(±2반음 time_stretch QC 보정은 예외).
- ④ 큐레이션 승인 없이 ⑤~⑧을 진행하지 않는다.
- 파괴적 작업(드라이브 파일 삭제 등)은 사용자가 직접 하거나 명시 요청 시에만.
- 도시명·폴더 ID·썸네일 파일명을 매 단계 `{city}`로 일관되게 치환했는지 확인한다.
