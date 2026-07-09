# City_ 장르 팔레트 — 채널 다양화 설계

> 2026-06-14. project.md의 "음색 템플릿 = 브랜드" 전략을 깨지 않으면서
> 다양성을 **장르 축**으로 확장하기 위한 문서. 기존엔 도시별 키/BPM/컬러 악기로만
> 다양화했으나 "다 비슷비슷"하다는 한계 → 같은 "도시 장면" 우산 아래
> **장면의 에너지·시간대**를 장르로 분화한다.

## 원칙 (브랜드 실은 유지)

- **유지(전 장르 공통)**: `no vocals` · `subtle vinyl warmth`(텍스처 연속성) ·
  `[MOOD] = 도시의 한 장면` 한 줄 · `도시명_` 타이포 + 실사 썸네일.
- **가변(장르 = 새 축)**: 드럼/베이스/리드·패드/화성 = 장르 정체성.
- **키는 조표 단순한 것 위주** (실측: A/E/D/C장조·Am/Em/Dm 준수율 높음,
  샤프·플랫 많은 키는 이탈). 마이너 장르도 Am(0)·Em(♯1)·Dm(♭1) 우선.
- **앰비언스는 후반작업** (Suno 프롬프트에 SFX 단어 금지). 장르별 레이어:
  재즈=비/카페, 하우스=도시 험·먼 사이렌·군중 웅성, 신스웨이브=테이프 히스,
  앰비언트=바람·먼 물소리. 전체에 −12~−18dB 한 레이어.
- **텍스처 분화(곡 단조로움 방지)**: 표준 4~5 / sparse 2 / lead·pad-forward 2 /
  break(드럼/킥 빠짐) 1. 장르별로 sparse·break의 의미만 달라진다.

---

## 1. Jazzhop — 현재 기준 (저녁·비·조용)

```
chill lofi jazz instrumental, [BPM] bpm, in [KEY], warm muffled electric piano chords,
soft mellow keys melody, deep round bass, dusty boom bap drums with quiet hats,
vinyl crackle, heavy lowpass filter, jazzy seventh chords with gentle 2-5-1 turnarounds,
[MOOD] mood, no vocals
```
- **BPM** 60~88 · **컬러** 뮤트 트럼펫 / 클라리넷 / 색소폰 / 나일론 기타
- **도시** Paris 자정, London 비, Prague 눈, Florence 저녁, Lisbon 오후

## 2. Deep / Melodic house — 심야·네온·클럽

```
melodic deep house instrumental, [BPM] bpm, in [KEY], warm analog synth chords,
deep round sub bass, soft four-on-the-floor kick, crisp closed hats and shaker groove,
lush airy pads, gentle filtered chord stabs, subtle vinyl warmth,
[MOOD] mood, no vocals
```
- **BPM** 118~122 · **컬러** plucked synth / rhodes stab / muted sax pad
- **sparse** = 브레이크다운(킥 빠지고 패드+베이스만) · **break** = 인트로/아웃트로 무킥
- **도시** Berlin 새벽 클럽, NYC 옥상 심야, Amsterdam 운하 야간, Seoul 강남 심야
- 샘플 (Berlin_ 새벽, Am):
```
melodic deep house instrumental, 122 bpm, in A minor, warm analog synth chords,
deep round sub bass, soft four-on-the-floor kick, crisp closed hats and shaker groove,
lush airy pads, gentle filtered chord stabs, subtle vinyl warmth,
cold concrete club glowing at 5am mood, no vocals
```

## 3. Organic / Downtempo house — 일몰·해변·따뜻함

```
organic deep house instrumental, [BPM] bpm, in [KEY], warm rhodes chords,
deep rolling bass, soft four-on-the-floor kick, organic shakers congas and woodblock groove,
marimba melody, lush warm pads, subtle vinyl warmth,
[MOOD] mood, no vocals
```
- **BPM** 108~116 · **컬러** marimba / kalimba / nylon guitar / pan flute
- **도시** Ibiza 일몰 애프터파티, Lisbon 오후, Havana 골든아워, Tulum
- 샘플 (Ibiza_ 일몰, C):
```
organic deep house instrumental, 112 bpm, in C major, warm rhodes chords,
deep rolling bass, soft four-on-the-floor kick, organic shakers congas and woodblock groove,
marimba melody, lush warm pads, subtle vinyl warmth,
last sun melting into the sea mood, no vocals
```

## 4. Synthwave / Chillwave — 레트로 네온

```
chill synthwave instrumental, [BPM] bpm, in [KEY], warm analog synth pads,
nostalgic lead synth melody, deep analog bass, soft gated drums with rim and claps,
retro arpeggios, subtle tape saturation and vinyl warmth,
[MOOD] mood, no vocals
```
- **BPM** 80~100 · **컬러** retro lead synth / FM bells
- **도시** Tokyo 네온, Miami 나이트, Seoul 강남 (재즈판 Tokyo와는 별개 장면으로)
- 샘플 (Miami_ 나이트, Am):
```
chill synthwave instrumental, 92 bpm, in A minor, warm analog synth pads,
nostalgic lead synth melody, deep analog bass, soft gated drums with rim and claps,
retro arpeggios, subtle tape saturation and vinyl warmth,
pink neon reflecting on wet boulevard mood, no vocals
```

## 5. Trip-hop — 어둡고 무거운·시네마틱

```
chill trip hop instrumental, [BPM] bpm, in [KEY], dusty electric piano chords,
deep heavy sub bass, slow head-nod drums with big snare and dusty hats,
melancholic strings and muted trumpet, vinyl crackle, heavy lowpass filter,
[MOOD] mood, no vocals
```
- **BPM** 82~92 · **컬러** muted trumpet / cello / harmonica
- **도시** London 심야, Bristol, Prague 비 갠 밤
- 샘플 (London_ 심야, Dm):
```
chill trip hop instrumental, 88 bpm, in D minor, dusty electric piano chords,
deep heavy sub bass, slow head-nod drums with big snare and dusty hats,
melancholic strings and muted trumpet, vinyl crackle, heavy lowpass filter,
fog rolling under amber street lamps mood, no vocals
```

## 6. Ambient (no drums) — 안개·새벽

```
ambient lofi instrumental, [BPM] bpm, in [KEY], soft felt piano,
warm evolving synth pads, deep round sub bass, no drums,
gentle vinyl crackle, heavy lowpass filter, slow jazzy chord movement,
[MOOD] mood, no vocals
```
- **BPM** 60~72(느리게) · **컬러** felt piano / celesta / glassy pad
- **도시** Kyoto 안개 새벽, Prague 눈, Venice 겨울 안개
- 세트 전체를 이걸로 가기보단 **다른 장르 세트 중반 "숨 고르기" 1~2곡**으로도 활용

---

## 도시 × 장르 매핑

| 도시/장면 | 장르 | 키(권장) | BPM | 컬러 | 상태 |
|---|---|---|---|---|---|
| Florence_ 저녁 | Jazzhop | — | — | — | 완성 |
| London_ 비 | Jazzhop | Dm+F | 63 | 펠트피아노/뮤트트럼펫 | 진행 중 |
| Paris_ 자정 | Jazzhop | Bb+Gm | 72 | 클라리넷 | 준비됨 |
| Tokyo_ 비갠 네온밤 | Jazzhop | Em+G | 84 | 에어리 패드 | 준비됨 |
| New York_ 심야 재즈바 | Jazzhop | Eb+Cm | 88 | 색소폰 | 준비됨 |
| Prague_ 눈 | Jazzhop | C+Am | 60 | 첼레스타 | 준비됨 |
| Lisbon_ 오후 트램 | Jazzhop | Am+C | 76 | 나일론 기타 | 준비됨 |
| **Berlin_ 새벽 클럽** | **Deep house** | Am+C | 122 | plucked synth | 준비됨 (prompts/berlin.md) |
| **NYC_ 옥상 심야** | **Deep house** | Em | 120 | rhodes stab | 신규 후보 |
| **Amsterdam_ 운하 야간** | **Deep house** | Dm | 120 | sax pad | 신규 후보 |
| **Ibiza_ 일몰** | **Organic house** | C+Am | 112 | marimba | 신규 후보 |
| **Havana_ 골든아워** | **Organic house** | C | 110 | nylon guitar | 신규 후보 |
| **Miami_ 나이트** | **Synthwave** | Am | 92 | retro lead | 신규 후보 |
| **Tokyo_ 네온(에너지판)** | **Synthwave** | Em | 90 | FM bells | 신규 후보 |
| **London_ 심야(다크판)** | **Trip-hop** | Dm | 88 | 뮤트 트럼펫 | 신규 후보 |
| **Kyoto_ 안개 새벽** | **Ambient** | C/Am | 64 | 첼레스타 | 신규 후보 |
| Seoul_ 강남 심야 | Deep house/Synthwave | Am | 118/92 | — | 후보(국내 유입) |

> 같은 도시를 두 장르로 내도 됨(Tokyo 재즈/신스웨이브, London 재즈/트립합) —
> "다른 시간·에너지의 같은 도시"라 시리즈 내 변주로 오히려 유리.

## 생성 운영 (project.md 승계)

1. Suno에서 **곡 제목을 목표곡명으로 직접 지정** 생성.
2. mp3 → `audio/suno/{city}/`.
3. **전곡 실측** → ±1~2반음 time_stretch 보정 / ±3 이상 재생성.
   하우스 BPM(118~122)은 Suno 준수율 높음, 키만 단순하게.
4. 세트 조립 후 장르별 앰비언스 1레이어 −12~−18dB.
