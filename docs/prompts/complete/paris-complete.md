# Paris_ — 자정의 파리 (완료 매니페스트)

> 테마: *"센강이 보이는 창가에서 맞는 자정의 파리."*
> ggg 공식: 서로 다른 곡 → 세트 ~23분 → ×2회 통반복 ≈ 45분.
> 소스는 4곡(변형 쌍 4세트, 총 8파일) — 4곡 모두 양쪽 테이크를 다 사용해 8슬롯 세트를 구성.
> 전곡 **72 BPM**, 본조 **Bb장조(A#) / F장조** + 관계 단조(A단조·D단조) 2곡으로 명암.
> 인접 트랙 같은키 0건이 되도록 F·Bb·단조를 교차 배치.
> ⚠️ 소스가 4곡뿐이라 세트가 23분으로 짧아 최종 길이는 **45:20**(통상 1시간 목표보다 짧음).
> 1시간을 원하면 곡 3~4개를 추가 생성해 세트를 ~30분으로 늘리면 된다.

## 산출물

| 항목 | 경로 | 비고 |
|---|---|---|
| 영상(mp4) | `audio/output/paris-1hour.mp4` | 129,638,366 B · 45:52 · 1920×1080 H.264 + AAC 48kHz 스테레오 |
| 오디오(wav) | `audio/output/paris-1hour.wav` | 522,409,540 B · 48kHz/16bit 스테레오 · 45.35분 · 세트 ×2 |
| 썸네일 | `image/paris-16x9.png` | 1920×1080 (16:9) · 인코딩용 축소본 |
| 고해상 원본 | `image/paris_16.png` | 10112×5688 (16:9) · higgsfield 편집본(어둡고 무드 있는 파리 야경) |
| 빌드 명령 | `python3 scripts/build_mix.py paris` | 무음 제거·중앙값 RMS 통일·등파워 3s 크로스페이드·세트 ×2·끝 8s 페이드·피크 리미터 |

### gdrive 백업 (바이트 검증 ✓)
- 최종본: `gdrive:paris/paris-1hour.mp4`, `gdrive:paris/paris-1hour.wav`
  (output 폴더 `1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R`) — 로컬과 바이트 일치 확인.
- 소스곡: `gdrive:paris/*.mp3` (suno 폴더 `143KPGQS8wRkUfuxJRFQ9FG-6-2cGuFt1`) — 8곡.

## 최종 트랙 리스트 (세트 1 타임스탬프)

| # | 시작 | 표시명(YouTube) | 소스 파일 | 키 | BPM* | 역할 |
|---|---|---|---|---|---|---|
| 1 | 00:00 | River Lamplight | River Lamplight | F장조 | 72 | **오프너(최장·클라리넷)** |
| 2 | 03:37 | Montmartre After Midnight | Montmartre After Midnight_1 | A#(Bb)장조 | 72 | 밝은 Bb |
| 3 | 06:11 | Attic Rooftops | Attic Rooftops_1 | F장조 | 72 | 지붕 위 다락 |
| 4 | 09:46 | Last Train Home | Last Train Home | A단조 | 72 | **단조 색채 ① · 중심** |
| 5 | 12:51 | Montmartre After Midnight (Reprise) | Montmartre After Midnight | A#(Bb)장조 | 72 | 밝게 회복 |
| 6 | 15:31 | River Lamplight (Reprise) | River Lamplight_1 | F장조 | 72 | 강가 재방문 |
| 7 | 17:46 | Last Train Home (Reprise) | Last Train Home_1 | D단조 | 72 | 단조 색채 ② |
| 8 | 20:01 | Attic Rooftops (Reprise) | Attic Rooftops | A#(Bb)장조 | 72 | 클로저(밝은 Bb) |
| — | 22:40 | — 세트 반복(×2) — | | | | |

\* 전곡 Suno에서 72 BPM 지정. 키 추정은 librosa 근사치(상대 참고용).
키 배열 `F·Bb·F·Am·Bb·F·Dm·Bb` → 인접 같은키 0건.
같은 곡의 두 테이크가 한 세트 안에 나오므로 뒤쪽은 (Reprise)로 표기.
소스 파일명은 `scripts/build_mix.py`의 `PROJECTS["paris"]` 기준.

## 유튜브 설명란 (복붙용)

```
Midnight in Paris from a window over the Seine — warm lofi jazz for late nights, studying, and slow evenings. 🌙

Track list:
00:00 River Lamplight
03:37 Montmartre After Midnight
06:11 Attic Rooftops
09:46 Last Train Home
12:51 Montmartre After Midnight (Reprise)
15:31 River Lamplight (Reprise)
17:46 Last Train Home (Reprise)
20:01 Attic Rooftops (Reprise)
22:40 — set repeats —

Music generated with Suno AI.

#lofi #lofihiphop #lofijazz #studymusic #paris #jazz #nightlofi #chillbeats #relaxingmusic #sleepmusic
```

## 업로드 체크리스트
- [ ] 제목: `Paris_ 🌙 Midnight in Paris Lofi — Warm Jazz to Study / Relax`
- [ ] 썸네일: `image/paris-16x9.png` (1920×1080, 16:9) — 고해상 원본은 `image/paris_16.png`
- [ ] **수익 창출 OFF** — Suno 무료 플랜은 비상업적 사용만 허용
- [ ] "아동용 아님(Not made for kids)" 설정
- [ ] 설명란에 위 Track list + "Music generated with Suno AI." 포함
- [ ] ⚠️ 길이 45:20 — 제목에 "[1 Hour]" 붙이지 말 것(정직성). 1시간이 필요하면 곡 추가 후 재빌드.

## 미사용 예비 곡
- 없음 — 소스 4곡(8파일)을 전부 사용. 다음 파리 확장 시 곡 3~4개 추가 생성 권장.

## 참고
- 원래 생성 기획(10곡 Bb장조 프롬프트)은 `paris-project.md`에 보존. 실제 생성은 4곡으로 진행됨.
