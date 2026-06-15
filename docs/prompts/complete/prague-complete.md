# Prague_ — 눈 내리는 프라하 (완료 매니페스트)

> 테마: *"따뜻한 창 너머로 보는 눈 내리는 프라하."*
> ggg 공식: 서로 다른 10곡 → 세트 ~29분 → ×2회 통반복 ≈ 59분.
> 소스 14곡(변형 쌍 7세트) 중 키·템포가 확연히 다른 쌍 3세트는 양쪽 다 사용,
> 거의 동일한 쌍은 하나만 채택. 이 컬렉션은 **G장조 편중**(14곡 중 8곡)이라
> 비G 곡(C장조·A단조·E단조)을 G곡 사이에 끼워 인접 같은키를 0건으로 맞췄다.

## 산출물

| 항목 | 경로 | 비고 |
|---|---|---|
| 영상(mp4) | `audio/output/prague-1hour.mp4` | 155,582,566 B · 58:41 · 1920×1080 H.264 + AAC 48kHz 스테레오 |
| 오디오(wav) | `audio/output/prague-1hour.wav` | 670,644,204 B · 48kHz/16bit 스테레오 · 58.22분 · 세트 ×2 |
| 썸네일 | `image/prague-16x9.png` | 10112×5688 (16:9) · 실물 사진 편집("Prague_" 타이틀) |
| 원본 이미지 | `image/prague.png` | 1376×768 · higgsfield 생성본(미사용, 백업용) |
| 빌드 명령 | `python3 scripts/build_mix.py prague` | 무음 제거·중앙값 RMS 통일·등파워 3s 크로스페이드·세트 ×2·끝 8s 페이드·피크 리미터 |

### gdrive 백업 (바이트 검증 ✓)
- 최종본: `gdrive:prague/prague-1hour.mp4`, `gdrive:prague/prague-1hour.wav`
  (output 폴더 `1FTLjGp59t6ylO2gSS12eHmatJBUzH3-R`) — 로컬과 바이트 일치 확인.
- 소스곡: `gdrive:prague/*.mp3` (suno 폴더 `143KPGQS8wRkUfuxJRFQ9FG-6-2cGuFt1`) — 14곡.

## 최종 트랙 리스트 (세트 1 타임스탬프)

| # | 시작 | 표시명(YouTube) | 소스 파일 | 키 | BPM* | 역할 |
|---|---|---|---|---|---|---|
| 1 | 00:00 | Frosted Window | Snowy Window Loop_1 | C장조 | 117 | 오프너 — 밝고 따뜻한 C |
| 2 | 02:23 | Cobblestone Lanes | Snow on Cobblestones | G장조 | 117 | 자갈길, 흐름 형성 |
| 3 | 06:00 | Old Town Square | Snow in the Square | E단조 | 117 | 단조 색채 ① |
| 4 | 08:24 | Bridge in the Mist | Snow Bridge Dust | G장조 | 60 | 템포 다운(슬로우) |
| 5 | 11:51 | **Castle Above Rooftops** | Castle Above Rooftops | A단조 | 123 | **중심곡(최장 4:03·단조 깊이)** |
| 6 | 15:50 | Square at Dusk | Snow in the Square_1 | G장조 | 89 | 회복·리프트 |
| 7 | 18:21 | Charles Bridge, Blue Hour | Snow Bridge Dust_1 | A단조 | 123 | 단조 색채 ② |
| 8 | 20:46 | Quiet Window | Snowy Window Loop | G장조 | 58 | 슬로우 와인드다운 |
| 9 | 23:01 | Last Tram Home | Snowy Tram Stop_1 | C장조 | 117 | 밝게 환기 |
| 10 | 25:49 | Warm Window Drift | Warm Window Drift | G장조 | 76 | 피날레 — 따뜻한 창가 |
| — | 29:06 | — 세트 반복(×2) — | | | | |

\* BPM은 librosa 옥타브 추정 오차(60↔120)가 섞여 상대 참고용.
키 배열 `C·G·E단·G·A단·G·A단·G·C·G` → 인접 같은키 0건.
표시명은 유튜브 공개용(소스 파일명은 `scripts/build_mix.py`의 `PROJECTS["prague"]` 기준).

## 유튜브 설명란 (복붙용)

```
Snowy Prague seen from a warm window — 1 hour of cozy lofi jazz for studying, reading, and slow winter nights. ❄️

Track list:
00:00 Frosted Window
02:23 Cobblestone Lanes
06:00 Old Town Square
08:24 Bridge in the Mist
11:51 Castle Above Rooftops
15:50 Square at Dusk
18:21 Charles Bridge, Blue Hour
20:46 Quiet Window
23:01 Last Tram Home
25:49 Warm Window Drift
29:06 — set repeats —

Music generated with Suno AI.

#lofi #lofihiphop #lofijazz #studymusic #prague #snow #winterlofi #chillbeats #relaxingmusic #sleepmusic
```

## 업로드 체크리스트
- [ ] 제목: `Prague_ ❄️ Snowy Prague Lofi — Cozy Winter Jazz to Study / Relax [1 Hour]`
- [ ] 썸네일: `image/prague-16x9.png` (1920×1080 이상, 16:9)
- [ ] **수익 창출 OFF** — Suno 무료 플랜은 비상업적 사용만 허용
- [ ] "아동용 아님(Not made for kids)" 설정
- [ ] 설명란에 위 Track list + "Music generated with Suno AI." 포함

## 미사용 예비 곡 (4곡 — 전부 잉여 G장조, 다음 도시 재활용)
- Castle Above Rooftops_1 (G장조 123, 4:47 — 실제 최장. G장조 중심곡이 필요하면 교체용)
- Snow on Cobblestones_1 (G장조 123, 1:44)
- Snowy Tram Stop (G장조 117, 2:45)
- Warm Window Drift_1 (G장조 161, 2:36 — 빠른 변형)
