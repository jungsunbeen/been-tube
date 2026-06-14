# Tokyo_ — 비 갠 네온 밤 (Suno 프롬프트 10곡)

> **E단조 본조 + G장조(관계조) 3곡, 전곡 84 BPM.** 컬러 악기: 에어리 신스 패드.
> ※ 원래 계획은 F#단조였으나 **1일차 실측에서 샤프 많은 키(F#장조/G#단조) 전부
> 키 이탈** → 같은 네온 무드를 내는 E단조(♯1개)로 변경. project.md 매핑도 갱신됨.

## 생성 규칙

1. Suno에서 곡 제목을 아래 제목 그대로 지정해서 생성.
2. 무드 줄에 rain/빗소리 단어 없음 — "비 갠 뒤"는 젖은 반사 이미지로만 표현 (앰비언스는 후반작업).
3. 생성 후 전곡 실측 → ±1~2반음 보정 / ±3 이상 재생성.
4. mp3는 `audio/suno/tokyo/`에 저장.

## 트랙 구성표

| # | 제목 | 키 | 텍스처 | 역할 |
|---|---|---|---|---|
| 1 | Neon Afterglow | Em | 표준, 멜로디 또렷 | 오프너 |
| 2 | Shibuya at 2AM | Em | 표준 | |
| 3 | Vending Machine Glow | Em | sparse drums | |
| 4 | Wet Asphalt Reflections | Em | 신스 패드 forward | |
| 5 | Konbini Light | **G장조** | 표준 | 중반 밝기 아치 |
| 6 | Quiet Side Street | **G장조** | sparse drums | |
| 7 | Last Train Platform | Em | **no drums** | 숨 고르기 |
| 8 | Rooftop Antennas | Em | 코드 중심 | |
| 9 | Tokyo Tower Distance | **G장조** | 신스 패드 forward | |
| 10 | First Light Skyline | Em | 가장 풍성 | 클로저 |

---

## 1. Neon Afterglow — Em (오프너) >> wet neon key
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
neon signs glowing on wet midnight streets mood, no vocals
```

## 2. Shibuya at 2AM — Em
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
empty crossing under glowing billboards mood, no vocals
```

## 3. Vending Machine Glow — Em (sparse) >> alley vending glow
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, sparse dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
lone vending machine light in a dark alley mood, no vocals
```

## 4. Wet Asphalt Reflections — Em (신스 패드) >> wet asphalt keys
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
airy synth pads, soft mellow keys melody, deep round bass, dusty boom bap drums
with quiet hats, vinyl crackle, heavy lowpass filter, jazzy seventh chords with
gentle 2-5-1 turnarounds, city colors smeared across wet asphalt mood, no vocals
```

## 5. Konbini Light — G장조 (밝기 아치) >> coner glow loop
```
chill lofi jazz instrumental, 84 bpm, in G major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
warm convenience store glow on a quiet corner mood, no vocals
```

## 6. Quiet Side Street — G장조 (sparse)
```
chill lofi jazz instrumental, 84 bpm, in G major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, sparse dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
narrow lantern-lit side street after midnight mood, no vocals
```

## 7. Last Train Platform — Em (no drums, 숨 고르기)
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, no drums, keys and bass only,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
empty platform after the last train mood, no vocals
```

## 8. Rooftop Antennas — Em (코드 중심)
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
minimal melody, chords forward, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
rooftop view of endless city lights mood, no vocals
```

## 9. Tokyo Tower Distance — G장조 (신스 패드) 
```
chill lofi jazz instrumental, 84 bpm, in G major, warm muffled electric piano chords,
airy synth pads, soft mellow keys melody, deep round bass, dusty boom bap drums
with quiet hats, vinyl crackle, heavy lowpass filter, jazzy seventh chords with
gentle 2-5-1 turnarounds, distant tower glowing through night haze mood, no vocals
```

## 10. First Light Skyline — Em (클로저) >> pale dawn turnaround 
```
chill lofi jazz instrumental, 84 bpm, in E minor, warm muffled electric piano chords,
soft mellow keys melody, airy synth pads, deep round bass,
dusty boom bap drums with quiet hats, vinyl crackle, heavy lowpass filter,
jazzy seventh chords with gentle 2-5-1 turnarounds,
pale dawn rising over the skyline mood, no vocals
```

---

## 생성 후 체크리스트

1. mp3 → `audio/suno/tokyo/` (제목 그대로)
2. 전곡 실측 → 보정/재생성 판정
3. 세트 순서 = 구성표 순서
4. 앰비언스(잦아드는 빗물 소리, 낮은 도시 험)는 세트 조립 후 전체에 -12~-18dB
