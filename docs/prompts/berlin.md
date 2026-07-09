# Berlin_ — 새벽 클럽이 끝난 뒤 (Suno 프롬프트 10곡 · Deep house) — v2

> **A단조 본조 + C장조(관계조) 3~4곡, 전곡 122 BPM.** 시리즈 첫 하우스 편.
> 장면 아치: 클럽 안(1–3) → 거리로(4) → 슈프레 강 새벽(5–6) → 여운(7) → 도시 아침(8–9) → 귀갓길 해돋이(10).
>
> **v2 개정 (2026-07-09, 1차 6곡 실측 반영):**
> - 1차 3프롬프트×6곡의 음색 유사도(MFCC)가 0.98~1.00 — 악기 줄이 같으면 하우스는
>   재즈합보다 훨씬 균질하게 들림(멜로디 밀도가 낮아 무드 줄만으론 분화 안 됨).
>   → **곡마다 리드/컬러 악기를 다르게 명시** (plucked / rhodes / sax pad / FM bells / organ).
> - "breakdown arrangement with no kick drum"은 Suno가 무시하고 4/4 킥을 넣음(2테이크 모두).
>   → 무킥 곡은 **장르 태그 자체를 변경** (atmospheric downtempo / ambient house) + 킥 부정어 중복.
> - 생성된 3곡(각 2테이크)은 음색·킥이 표준 규격이라 **표준 슬롯(1~3)으로 재배치**, 폐기 없음.

## 생성 규칙

1. Suno에서 곡 제목을 아래 제목 그대로 지정해서 생성. **#4~#10만 신규 생성** (1~3은 완료).
2. 무드 줄에 군중 웅성/사이렌 등 SFX 단어 없음 — 의도된 것 (앰비언스는 후반작업:
   도시 험·먼 사이렌·군중 웅성 1레이어 −12~−18dB).
3. 생성 후 전곡 실측 → ±1~2반음 보정 / ±3 이상 재생성.
4. **하우스 전용 QC**: #6(브레이크다운)·#7(beatless)에 four-on-the-floor 킥이 들어가면
   재생성. 반대로 표준 곡(#4,5,8,9,10)에 킥이 없어도 재생성.
5. **파일은 mp3로 저장** → `audio/suno/berlin/`. m4a로 받았으면 mp3 변환 필요
   (실측·rclone 백업·build_mix가 전부 `*.mp3` 기준).

## 트랙 구성표

| # | 제목 | 키 | 컬러/텍스처 | 역할 | 상태 |
|---|---|---|---|---|---|
| 1 | Concrete Dawn Loop | Am | plucked, 표준 | 오프너 | ✅ 생성됨 (Am 5.3분 / D장조 6.4분 테이크) |
| 2 | Basement Drift | C | 표준 | | ✅ 생성됨 (D장조 3.5분 / C장조 2.5분 테이크) |
| 3 | Smoke Through Strobe | Am | 표준 (킥 포함, 브레이크다운→표준 재배치) | | ✅ 생성됨 (C장조 3.7분 / Am 3.8분 테이크) |
| 4 | Kreuzberg Wires | Am | **rhodes 스탭, 코드 중심** | | 신규 |
| 5 | First Light on the Spree | **C** | **muted sax pad, 패드 포워드** | 중반 밝기 아치 | 신규 |
| 6 | Oberbaum Crossing | **C** | **브레이크다운 (무킥, 강화 표현)** | | 신규 |
| 7 | Afterhours Hallway | Am | **beatless (no drums, 강화 표현)** | 숨 고르기 | 신규 |
| 8 | Plattenbau Sky | Am | **FM bells 멜로디** | | 신규 |
| 9 | Fernsehturm Blink | Am | **warm organ 스탭 + plucked 악센트** | | 신규 |
| 10 | Sunrise on Warschauer Brücke | **C** | 가장 풍성 (plucked+rhodes+sax) | 클로저 | 신규 |

> 키 집계(테이크 선택에 따라): Am 5~6곡 + C 4~5곡. D장조 테이크는 −2반음 보정하면
> C장조로 편입 가능(±2 범위 내, 투명). 테이크 선택·보정은 ④ 큐레이션에서 확정.

---

## 1~3. 생성 완료 (1차 프롬프트, 표준 텍스처)

Concrete Dawn Loop · Basement Drift · Smoke Through Strobe — 각 2테이크가
`audio/suno/berlin/`에 있음(m4a → mp3 변환 필요). 전곡 123 BPM, 4/4 킥, 음색 동일 계열.
테이크 쌍 중 하나만 사용, 미사용 테이크는 예비로 기록.

## 4. Kreuzberg Wires — Am (rhodes 스탭, 코드 중심)
```
melodic deep house instrumental, 122 bpm, in A minor, warm rhodes chord stabs,
minimal melody, chords forward, deep round sub bass, soft four-on-the-floor kick,
crisp closed hats and shaker groove, gentle lowpass filtered pads,
subtle vinyl warmth, tangled wires over quiet Kreuzberg streets at dawn mood, no vocals
```

## 5. First Light on the Spree — C (muted sax pad, 밝기 아치)
```
melodic deep house instrumental, 122 bpm, in C major, warm analog synth chords,
soft muted saxophone pad phrases, deep round sub bass, soft four-on-the-floor kick,
crisp closed hats and shaker groove, lush airy pads,
subtle vinyl warmth, first pale light spreading over the river mood, no vocals
```

## 6. Oberbaum Crossing — C (브레이크다운, 무킥 — 강화 표현)
```
atmospheric downtempo house breakdown instrumental, 122 bpm, in C major,
no kick drum, kickless groove with soft shakers and closed hats only,
warm analog synth chords, deep round sub bass and lush airy pads carrying the flow,
subtle vinyl warmth, walking across the old brick bridge at sunrise mood, no vocals
```

## 7. Afterhours Hallway — Am (beatless, 숨 고르기 — 강화 표현)
```
ambient house instrumental, 122 bpm, in A minor, no drums at all, beatless,
warm evolving analog pads, soft glassy synth phrases, deep round sub bass,
gentle filtered chord movement, subtle vinyl warmth,
long empty corridor when the night ends mood, no vocals
```

## 8. Plattenbau Sky — Am (FM bells)
```
melodic deep house instrumental, 122 bpm, in A minor, warm analog synth chords,
nostalgic FM bell melody, deep round sub bass, soft four-on-the-floor kick,
crisp closed hats and shaker groove, lush airy pads,
subtle vinyl warmth, prefab tower blocks against a violet morning sky mood, no vocals
```

## 9. Fernsehturm Blink — Am (warm organ 스탭)
```
melodic deep house instrumental, 122 bpm, in A minor, warm organ chord stabs,
soft plucked synth accents, deep round sub bass, soft four-on-the-floor kick,
crisp closed hats and shaker groove with subtle percussion, gentle lowpass filtered pads,
subtle vinyl warmth, TV tower blinking over sleeping rooftops mood, no vocals
```

## 10. Sunrise on Warschauer Brücke — C (클로저, 가장 풍성)
```
melodic deep house instrumental, 122 bpm, in C major, warm analog synth chords,
bright plucked synth melody, gentle rhodes stabs, soft muted saxophone pad,
deep round sub bass, soft four-on-the-floor kick, crisp closed hats and shaker groove,
lush airy pads, subtle vinyl warmth,
morning sun flooding the bridge on the walk home mood, no vocals
```

---

## 생성 후 체크리스트

1. mp3 → `audio/suno/berlin/` (제목 그대로, m4a 금지)
2. 전곡 실측 → 보정/재생성 판정 (+ 킥 QC: 규칙 4 — 특히 #6, #7)
3. 세트 순서 = 구성표 순서, 28분 미만이면 예비 테이크 추가
   (1~3의 미사용 테이크가 예비 1순위)
4. **이음새 주의**: four-on-the-floor 킥은 재즈합보다 크로스페이드 3초 구간에서
   킥 겹침(플램)이 드러나기 쉬움 — 세트 조립 후 트랙 경계 청취 확인,
   거슬리면 무킥 곡(#6, #7)이 경계에 오도록 순서 재조정
5. 앰비언스(도시 험, 먼 사이렌, 군중 웅성)는 세트 조립 후 전체에 −12~−18dB
