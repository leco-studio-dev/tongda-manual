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
| 리포트는 **PDF 저장만** 가능 | UI 런처가 `CreateDocument("application/pdf")` 하나뿐 (`ui/settings/SettingsScreen.kt`, `ui/detail/DetailScreen.kt`). ViewModel 의 `exportReportToUri`(HTML 쓰기)와 `report_format_*` 문자열은 호출되지 않는 잔재이므로, 이 죽은 경로를 살리기 전까지 문서에 HTML 저장을 쓰지 말 것 |
| 화면 용어 (한/영) | `res/values/strings.xml`, `res/values-en/strings.xml` |
| 길게 눌러 삭제(wiggle) | `ui/common/WiggleChip.kt` + 호출부 3곳: `ui/issue/IssueSelectScreen.kt`(이슈, 확인 다이얼로그 있음), `ui/record/RecordScreen.kt`(증상 칩), `ui/treatment/TreatmentScreen.kt`(처치 칩). 칩 ⊖ 는 **직접 추가 항목=삭제 / 기본 항목=숨김**(`setSymptomEnabled(false)` / `setItemEnabled(false)`)으로 분기 |
| 숨긴 기본 항목은 복구 불가 | `setSymptomEnabled(…, true)` 를 호출하는 UI 가 없다. 같은 이름 재추가도 `disabled` 필터에 걸려 안 나타난다 (`data/prefs/SymptomRepository.kt` `effectiveSymptomsByCategory`) |
| 기록 수정·삭제 진입점 | `ui/detail/DetailScreen.kt` 상단바 ✏️/🗑 (대상 = 현재 보고 있는 `recordId`), `ui/treatment/TreatmentDetailScreen.kt` 편집/삭제. 편집 저장 시 경고 다이얼로그 = `RecordScreen.kt:245`, `TreatmentScreen.kt` |
| 이슈 이름·상태 변경 없음 | 생성 시 `status = "Active"` 고정(`ui/issue/IssueSelectViewModel.kt:77`), rename/status 변경 호출부 없음 |

## 스크린샷

`assets/img/ko/`, `assets/img/en/` — 언어별 13장, **720px 폭 PNG**(합계 약 1.4MB).
vc196 · Pixel 1080×2400 에뮬레이터에서 언어별로 샘플 데이터를 새로 주입해 촬영했다.

UI 가 바뀌면 다시 촬영해야 한다. 순서:

1. 에뮬레이터 부팅 → 디버그 APK 설치
2. 상태바 정리 (시계 09:30 고정, 알림 숨김):
   ```
   adb shell am broadcast -a com.android.systemui.demo -e command enter
   adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0930
   adb shell am broadcast -a com.android.systemui.demo -e command notifications -e visible false
   ```
3. 설정에서 언어 선택 → **개발 도구 → 전부 삭제 후 주입** (샘플 시드는 로케일 대응이라
   선택한 언어로 이슈명·메모가 들어간다). 언어를 바꿀 때마다 다시 주입할 것.
4. `adb exec-out screencap -p` 로 캡처 → `sips -Z 720` 로 리사이즈해 같은 파일명으로 덮어쓴다.
   파일명은 문서의 `<img src>` 와 1:1 이므로 **이름을 바꾸지 말 것**.

바디맵 이미지는 "한 기록에 여러 강도"를 보여주려고 허리를 7, 다리를 4로 칠한 것이다.
처치 상세 이미지는 전후 6시간 규칙이 실제로 표시되는 사례를 골랐다. 다시 찍을 때도
같은 의도를 유지해야 캡션과 어긋나지 않는다.
