# tongda-manual

통다(Tongda) 앱 사용 설명서 — GitHub Pages 정적 사이트.

- 한국어: https://choi32013.github.io/tongda-manual/ko/
- English: https://choi32013.github.io/tongda-manual/en/
- 루트(`/`)는 브라우저 언어에 따라 위 두 곳으로 리다이렉트하며, JS가 꺼져 있으면 언어 선택 화면을 보여준다.

## 앱에서 열리는 경로

설정 → 앱 정보 → **메뉴얼 보기**. 앱은 `manual_url` 문자열 리소스를 열며,
`values/`는 `/ko/`, `values-en/`는 `/en/` 를 가리킨다. 즉 **앱 내 언어 설정을 따라간다**
(기기 언어가 아니라 `LocaleManager` 가 적용한 언어).

## 수정 방법

`main` 브랜치에 push 하면 Pages 가 바로 반영한다(보통 1분 이내). **앱 릴리스는 필요 없다.**

```
ko/index.html      한국어 본문
en/index.html      영어 본문
assets/manual.css  공용 스타일 (라이트/다크 자동)
index.html         루트 — 언어 리다이렉트 + 폴백 선택 화면
```

두 언어 문서는 **같은 섹션 구성과 같은 앵커 id** 를 쓴다(`#pain`, `#effect`, …).
한쪽만 고치면 언어 스위처로 오갈 때 내용이 어긋나므로, 구조를 바꿀 때는 양쪽을 함께 고칠 것.

## 내용을 고칠 때 주의

본문의 수치·규칙은 앱 코드에서 확인한 값이다. 앱을 바꿨으면 여기도 갱신해야 한다.

| 문서 내용 | 근거 (Tongda 레포 `app_dev`) |
|---|---|
| 하루 기록 3건, 통증 이슈 2개, 통계 30일 | `data/prefs/FreeLimitsRepository.kt` |
| 처치 효과 전후 6시간 규칙 | `report_effect_disclaimer`, `treatment_detail_effect_note` |
| 강도 색상 공식 (1~10) | `ui/common/IntensityBadge.kt` |
| 백업 `.tngd` 형식 · 10MB 한도 | `data/backup/BackupRepository.kt` |
| 리포트 구성 항목 | `data/backup/HtmlReportRepository.kt` |
| 화면 용어 (한/영) | `res/values/strings.xml`, `res/values-en/strings.xml` |

## 아직 없는 것

- 스크린샷 — 텍스트 우선으로 만들었다. 추가할 때는 한/영 화면을 각각 캡처하고
  longest edge ≤ 1800px 로 리사이즈해 `assets/img/` 에 두고 `<img>` 로 삽입한다.
