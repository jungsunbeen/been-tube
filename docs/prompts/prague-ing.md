# Prague_ — 눈 오는 밤 (Suno 프롬프트 10곡)

> **C장조 본조 + A단조(관계조) 3곡, 전곡 60 BPM.** 컬러 악기: 첼레스타/뮤직박스.
> 조표 0개로 가장 안전한 키 + 시리즈 최저 템포 (가장 절제된 영상).
> 겨울 시즌(11~1월) 공개 타깃 — "cozy winter jazz" 수요.

## 생성 규칙

1. Suno에서 곡 제목을 아래 제목 그대로 지정해서 생성.
2. 무드 줄의 snow는 시각 이미지로만 사용 (눈소리 SFX 요청 아님 — 앰비언스는 후반작업).
3. 생성 후 전곡 실측 → ±1~2반음 보정 / ±3 이상 재생성.
4. mp3는 `audio/suno/prague/`에 저장.

## 트랙 구성표

| # | 제목 | 키 | 텍스처 | 역할 |
|---|---|---|---|---|
| 1 | Hushed Snowfall | C | 표준, 멜로디 또렷 | 오프너 |
| 2 | Old Town Square at Night | C | 표준 | |
| 3 | Lamplit Cobblestones | C | sparse drums | |
| 4 | Music Box Memory | C | 첼레스타 melody-forward | |
| 5 | Charles Bridge Statues | **Am** | 표준 | 중반 음영 아치 |
| 6 | Castle on the Hill | **Am** | sparse drums | |
| 7 | Empty Tram Stop | C | **no drums** | 숨 고르기 |
| 8 | Chimneys and Spires | C | 코드 중심 | |
| 9 | Astronomical Clock | **Am** | 첼레스타 melody-forward | |
| 10 | Midnight Snow Glow | C | 가장 풍성 | 클로저 |

---

## 1. Hushed Snowfall — C (오프너)
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, muffled sparse boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
hushed snow drifting past a warm window mood, no vocals
```

## 2. Old Town Square at Night — C
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, muffled dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
empty old town square under falling snow mood, no vocals
```

## 3. Lamplit Cobblestones — C (sparse)
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, sparse dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
snow gathering on lamplit cobblestones mood, no vocals
```

## 4. Music Box Memory — C (첼레스타)
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
delicate celesta melody like a music box, deep round bass, muffled dusty boom bap drums
with quiet hats, vinyl crackle, heavy lowpass filter, jazzy seventh chords with
gentle 2-5-1 turnarounds, nostalgic winter memory mood, no vocals
```

## 5. Charles Bridge Statues — Am (음영 아치)
```
chill lofi jazz instrumental, 60 bpm, in A minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, muffled dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
silent statues lining a snowy bridge mood, no vocals
```

## 6. Castle on the Hill — Am (sparse)
```
chill lofi jazz instrumental, 60 bpm, in A minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, sparse dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
distant castle glowing above the rooftops mood, no vocals
```

## 7. Empty Tram Stop — C (no drums, 숨 고르기)
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, no drums, keys and bass only,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
waiting alone at a snowy tram stop mood, no vocals
```



---- 여기까지함 6월 11일

## 8. Chimneys and Spires — C (코드 중심)
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
minimal melody, chords forward, deep round bass, muffled dusty boom bap drums with
quiet hats, vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle
2-5-1 turnarounds, smoke rising from snowy rooftops mood, no vocals
```

## 9. Astronomical Clock — Am (첼레스타)
```
chill lofi jazz instrumental, 60 bpm, in A minor, warm muffled electric piano chords,
delicate celesta melody like a music box, deep round bass, muffled dusty boom bap drums
with quiet hats, vinyl crackle, heavy lowpass filter, jazzy seventh chords with
gentle 2-5-1 turnarounds, ancient clock ticking past midnight mood, no vocals
```

## 10. Midnight Snow Glow — C (클로저)
```
chill lofi jazz instrumental, 60 bpm, in C major, warm muffled electric piano chords,
soft mellow keys melody, delicate celesta accents, deep round bass,
muffled dusty boom bap drums with quiet hats, vinyl crackle, heavy lowpass filter,
jazzy seventh chords with gentle 2-5-1 turnarounds,
city glowing soft orange under midnight snow mood, no vocals
```

---

## 생성 후 체크리스트

1. mp3 → `audio/suno/prague/` (제목 그대로)
2. 전곡 실측 → 보정/재생성 판정
3. 세트 순서 = 구성표 순서
4. 앰비언스는 가장 절제 — 낮은 겨울 바람만 아주 희미하게 (-18dB 이하), 또는 무음
