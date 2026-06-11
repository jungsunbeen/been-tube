# Suno 프롬프트 — "Paper" 시리즈 8곡 추가

ggg-analy.md 공식 적용: 서로 다른 곡 10개로 30분 세트 구성 → 2회 반복.
보유 중인 Paper Sun(C장조 81bpm), Paper Moon(D#단조 81bpm)에 8곡을 더한다.

## 베이스 템플릿 (Paper Sun/Moon에 쓴 원본 프롬프트)

```
chill lofi hip hop instrumental, 80 bpm, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, nostalgic late night mood, no vocals
```

새 8곡은 이 템플릿을 그대로 유지하고 **조성·BPM·무드 한 줄만 교체**한다.
→ 악기·질감이 동일해서 한 채널 사운드로 묶임.

공통 주의:
- Suno는 조성을 정확히 따르지 않을 수 있음 → 생성 후 `analyze_chords.py`로 측정,
  ±1~2반음 어긋나면 time_stretch로 보정 (이 정도는 음질 손실 거의 없음)
- 곡 길이는 2~4분 (3분 전후가 이상적)
- 프롬프트 1번당 2곡 출력 → 둘 중 나은 쪽을 채택, 나머지는 예비로 보관
  (Paper Sun/Moon처럼 둘 다 좋고 조성이 다르면 둘 다 써도 됨)

## 생성 일정 (하루 10곡 = 프롬프트 5번 제한)

| 날짜 | 프롬프트 | 곡 |
|---|---|---|
| 1일차 (2026-06-11) | #1~#5 | Paper Dawn, Plane, Boat, Rain, Lantern |
| 2일차 (2026-06-12) | #6~#8 + 예비 2번 | Paper Train, Snow, Stars + 1일차 실패작 재생성 |

2일차 남는 2번은 1일차 결과 중 조성이 크게 어긋났거나(±3반음 이상) 마음에
안 드는 곡을 다시 뽑는 데 쓴다.

| # | 제목(안) | 목표 조성 | 목표 BPM | 역할 |
|---|---|---|---|---|
| 1 | Paper Dawn | A장조 | 83 | 오프너 (ggg 시그니처) |
| 2 | Paper Plane | E장조 | 95 | 업템포 |
| 3 | Paper Boat | F#장조 | 70 | 차분한 구간 |
| 4 | Paper Rain | G#단조 | 90 | 단조 무드 |
| 5 | Paper Lantern | B장조 | 75 | 따뜻한 중반 |
| 6 | Paper Train | D장조 | 92 | 리듬감 |
| 7 | Paper Snow | F단조 | 76 | 플랫계 1곡 (색 변화) |
| 8 | Paper Stars | A장조 | 99 | 클로저 (홈 복귀, 최고 템포) |

---

## 1. Paper Dawn — A장조 83bpm (오프너)
> 함
```
chill lofi hip hop instrumental, 83 bpm, in A major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, gentle early morning mood, no vocals
```

## 2. Paper Plane — E장조 95bpm
> 함
```
chill lofi hip hop instrumental, 95 bpm, in E major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, hopeful daydream mood with light swing, no vocals
```

## 3. Paper Boat — F#장조 70bpm
> 함

```
chill lofi hip hop instrumental, 70 bpm, in F sharp major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, sparse dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, sleepy floating-on-water mood, no vocals
```

## 4. Paper Rain — G#단조 90bpm
>함
```
chill lofi hip hop instrumental, 90 bpm, in G sharp minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, bittersweet rainy evening mood, no vocals
```

## 5. Paper Lantern — B장조 75bpm
>함
```
chill lofi hip hop instrumental, 75 bpm, in B major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, cozy lantern-lit night mood, no vocals
```

## 6. Paper Train — D장조 92bpm
>함
```
chill lofi hip hop instrumental, 92 bpm, in D major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, steady dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, train window scenery mood with forward motion, no vocals
```

## 7. Paper Snow — F단조 76bpm (플랫계)
>함
```
chill lofi hip hop instrumental, 76 bpm, in F minor, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, muffled dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, hushed quiet snowfall at dusk mood, no vocals
```

## 8. Paper Stars — A장조 99bpm (클로저)

```
chill lofi hip hop instrumental, 99 bpm, in A major, warm muffled electric piano chords,
soft mellow keys melody, deep round bass, lively dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, bright starry night finale mood, no vocals
```

---

## 생성 후 체크리스트

1. mp3를 `audio/suno/`에 저장 (Paper Dawn.mp3 형식)
2. `analyze_chords.py`로 실제 조성·BPM 측정
3. 목표와 ±1~2반음/±10% 이내면 time_stretch로 보정, 그 이상 어긋나면 재생성
4. 10곡 → 약 30분 세트 구성 (mix1hour.py 개편: 변주 순환 → 트랙 나열 + 세트 2회 반복)
