# Berlin_ — 새벽 클럽이 끝난 뒤 (완료 매니페스트)

> 테마: *"클럽이 막 문을 닫은 블루아워의 베를린 거리, 걸어서 집으로."*
> **시리즈 첫 하우스 편** (melodic deep house). ggg 공식: 서로 다른 8슬롯 세트 ~32.7분 → ×2회 통반복 ≈ **1:05:19**(wav).
> 소스 6곡(테이크 쌍 6세트, 총 12파일) 중 8슬롯 사용 — paris 전례대로 2곡은 양쪽 테이크를 모두 사용.
> 전곡 **123 BPM**(목표 122, Suno 실측 123 완벽 통일), 키는 D장조 3 · C장조 3 · A단조 1 · F장조 1로
> 인접 트랙 같은키 0건 배치(D–Am–C–D–C–F–C–D).

## 산출물

| 항목 | 경로 | 비고 |
|---|---|---|
| 영상(mp4) | `gdrive:berlin/berlin-1hour.mp4` | 167,038,323 B · 1:05:53 · 1920×1080 H.264 + AAC 48kHz 스테레오 · **로컬 삭제됨(2026-07-09)** |
| 오디오(wav) | `gdrive:berlin/berlin-1hour.wav` | 752,447,564 B · 48kHz/16bit 스테레오 · 65.32분 · 세트 ×2 · **로컬 삭제됨(2026-07-09)** |
| 썸네일 | `image/berlin-16x9.png` | 1920×1080 (16:9) · 원본 센터 크롭 |
| 고해상 원본 | `image/berlin.png` | 10096×5636 · 나노바나나 생성(블루아워 거리 + "Berlin_" 타이포 포함) |
| 빌드 명령 | `python3 scripts/build_mix.py berlin` | 무음 제거·중앙값 RMS 통일·등파워 3s 크로스페이드·세트 ×2·끝 8s 페이드·피크 리미터 |

### gdrive 백업 (바이트 검증 ✓)
- 최종본: `gdrive:berlin/berlin-1hour.mp4`, `gdrive:berlin/berlin-1hour.wav`
  (output 폴더 `1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R`) — 로컬과 바이트 일치 확인.
  - mp4 링크: https://drive.google.com/open?id=15UJ7zgrEKzM1835OcGqnOBln_dfIRmMy
  - wav 링크: https://drive.google.com/open?id=13tgB-ZOGhE9knVNpXbtN407rVVmRRjpK
- 소스곡: `gdrive:berlin/*.mp3` (suno 폴더 `143KPGQS8wRkUfuxJRFQ9FG-6-2cGuFt1`) — 12파일.

## 최종 트랙 리스트 (세트 1 타임스탬프)

| # | 시작 | 표시명(YouTube) | 소스 파일 | 키 | BPM* | 역할 |
|---|---|---|---|---|---|---|
| 1 | 00:00 | Basement | Basement Drift | D장조 | 123 | 오프너(밝게 진입) |
| 2 | 03:25 | Smoke | Smoke Through Strobe_1 | A단조 | 123 | 단조 색채(클럽 심연) |
| 3 | 07:09 | Corridor | Corridor After Midnight_1 | C장조 | 123 | 리프트 |
| 4 | 11:19 | Concrete | Concrete Dawn Loop_1 | D장조 | 123 | **중심곡(최장 6:21)** |
| 5 | 17:37 | Strobe | Smoke Through Strobe | C장조 | 123 | 중반 환기 |
| 6 | 21:19 | Bridge | Brick Bridge Sunrise_1 | F장조 | 123 | **저킥 브레이크다운(숨 고르기)** |
| 7 | 24:59 | Drift | Basement Drift_1 | C장조 | 123 | 짧은 밝은 리프트 |
| 8 | 27:25 | Kreuzberg | Kreuzberg Dawn Wires_1 | D장조 | 123 | 클로저(rhodes 풍성) |
| — | 32:39 | — 세트 반복(×2) — | | | | |

유튜브 표시명은 소스 파일명과 무관하게 간단한 새 단어로 짓는다(테이크 구분 II 없음).
소스 파일명은 `scripts/build_mix.py`의 `PROJECTS["berlin"]` 기준.

## 유튜브 설명란 (복붙용)

```
The clubs just closed — walking home through blue hour Berlin. Melodic deep house for late nights, studying, and slow mornings. 🌆

Track list:
00:00 Basement
03:25 Smoke
07:09 Corridor
11:19 Concrete
17:37 Strobe
21:19 Bridge
24:59 Drift
27:25 Kreuzberg
32:39 — set repeats —

Music generated with Suno AI.

#deephouse #melodichouse #housemusic #berlin #chillhouse #studymusic #nightdrive #electronicmusic #relaxingmusic #afterhours
```

## 업로드 체크리스트
- [ ] 제목: `house list | Project Berlin_` (채널 제목 관례: `{장르} list | Project {도시}_`, 예: `jazz list | Project Prague_`)
- [ ] 썸네일: `image/berlin-16x9.png` (1920×1080, 16:9) — 고해상 원본은 `image/berlin.png`
- [ ] **수익 창출 OFF** — Suno 무료 플랜은 비상업적 사용만 허용
- [ ] "아동용 아님(Not made for kids)" 설정
- [ ] 설명란에 위 Track list + "Music generated with Suno AI." 포함
- [ ] ⚠️ 업로드 전 이음새 청취 권장 — 4/4 킥 곡 간 크로스페이드 플램 여부 (특히 11:19, 17:37, 27:25 부근). 자동 점검은 미완(사용자 중단).

## 미사용 예비 곡 (다음 확장/도시 재활용)

| 파일 | 키 | 길이 | 메모 |
|---|---|---|---|
| Brick Bridge Sunrise.mp3 | C장조 | 2:09 | 브레이크다운 의도였으나 4/4 킥 들어감 → 표준용 예비 |
| Concrete Dawn Loop.mp3 | A단조 | 5:15 | 중심곡의 다른 테이크 |
| Corridor After Midnight.mp3 | A단조 | 5:52 | beatless 의도였으나 4/4 킥 들어감 → 표준용 예비 |
| Kreuzberg Dawn Wires.mp3 | G장조 | 5:23 | 클로저의 다른 테이크 |

## 참고 (하우스 편에서 배운 것 — 다음 하우스 도시에 적용)

- 생성 기획은 `docs/prompts/berlin.md`(v2) 보존. 계획 10곡 중 6곡(12파일)으로 진행,
  #5(sax pad)·#8(FM bells)·#9(organ)·#10(클로저)은 미생성 — 다음 확장 시 후보.
- **음색 균질 이슈**: 같은 악기 줄의 프롬프트로는 하우스 곡들이 매우 비슷하게 들림(MFCC 0.98+).
  곡별 리드/컬러 악기를 다르게 명시해야 분화됨 (v2 개정 근거).
- **무킥 프롬프트 준수율 낮음**: "no kick drum"·"beatless"·장르 태그 변경까지 써도
  4테이크 중 1개만 저킥으로 나옴(Brick Bridge Sunrise_1, 비트락 0.22). 무킥 곡은 여분 생성 필요.
- BPM 준수율은 완벽(전곡 123), 키도 조표 0~2 내로 준수 — 재생성 0건.
