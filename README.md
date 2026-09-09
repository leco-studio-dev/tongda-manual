# tongda-manual

통다(Tongda) 앱 사용 설명서 — GitHub Pages 정적 사이트.

- 한국어: https://leco-studio-dev.github.io/tongda-manual/ko/
- English: https://leco-studio-dev.github.io/tongda-manual/en/
- 루트(`/`)는 브라우저 언어에 따라 위 두 곳으로 리다이렉트하며, JS가 꺼져 있으면 언어 선택 화면을 보여준다.

## 리포 위치 (2026-07-31 이전)

본문은 이 리포(`leco-studio-dev/tongda-manual`)에 있다. 예전 `choi32013/tongda-manual` 은
**리다이렉트 스텁만 남긴 채 살아 있으며 삭제하면 안 된다** — 앱 vc196 에 옛 주소가 박혀
배포됐기 때문에, 그 버전 사용자의 "메뉴얼 보기" 가 그 경로를 통해 여기로 넘어온다.
앱은 vc197 부터 이 주소를 직접 가리킨다.

`choi32013` 은 이 리포의 협업자(write)다. **Pages 설정 등 리포 설정 변경은 소유자
(leco-studio-dev) 계정으로만 가능**하다는 점만 유의.

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
| 기록 무제한(하루 한도 없음, v230), 통증 이슈 2개, 사진 이슈당 1장, 통계 30일 | `data/prefs/FreeLimitsRepository.kt` — 강제되는 무료 제한은 `MAX_ACTIVE_ISSUES`·`FREE_ATTACHMENTS_PER_ISSUE`·`FREE_STATS_DAYS` 셋뿐 |
| 무료 리포트도 최근 30일 (v230) | `data/backup/ReportWindow.kt` + `HtmlReportRepository.generate` 가 `statsFloorDateFresh()` 로 재단, `report_free_window_note` |
| 광고는 보상형 4곳(이슈 추가·사진 추가·리포트 내보내기·백업 내보내기), 배너 없음 | `ads/RewardedAdManager.Slot`, `ui/common/AdGateDialog.kt`, `ui/common/ExportAdGate.kt` (리포트는 설정·상세 두 입구 모두 게이트, v231) |
| 처치 효과 전후 **48시간** 규칙 + 한 쌍은 가장 앞선 처치 하나에만 귀속 (v228~229) | `ui/stats/TreatmentEffect.kt` (`WINDOW_HOURS`, `samples()`), `report_effect_disclaimer`, `treatment_detail_effect_note` |
| 강도 색상 공식 (1~10) | `ui/common/IntensityBadge.kt` |
| 백업 `.tngd` 형식 · 10MB 한도 | `data/backup/BackupRepository.kt` |
| 리포트 구성 항목 | `data/backup/HtmlReportRepository.kt` |
| 리포트는 **PDF 저장만** 가능 | UI 런처가 `CreateDocument("application/pdf")` 하나뿐 (`ui/settings/SettingsScreen.kt`, `ui/detail/DetailScreen.kt`). ViewModel 의 `exportReportToUri`(HTML 쓰기)와 `report_format_*` 문자열은 호출되지 않는 잔재이므로, 이 죽은 경로를 살리기 전까지 문서에 HTML 저장을 쓰지 말 것 |
| 화면 용어 (한/영) | `res/values/strings.xml`, `res/values-en/strings.xml` |
| 길게 눌러 관리 | `ui/common/WiggleChip.kt` + 호출부 3곳: `ui/issue/IssueSelectScreen.kt`(이슈 관리 → 이름 변경 또는 삭제 확인), `ui/record/RecordScreen.kt`(증상 칩), `ui/treatment/TreatmentScreen.kt`(처치 칩). 칩 ⊖ 는 **직접 추가 항목=삭제 / 기본 항목=숨김**(`setSymptomEnabled(false)` / `setItemEnabled(false)`)으로 분기 |
| 숨긴 기본 항목은 복구 불가 | `setSymptomEnabled(…, true)` 를 호출하는 UI 가 없다. 같은 이름 재추가도 `disabled` 필터에 걸려 안 나타난다 (`data/prefs/SymptomRepository.kt` `effectiveSymptomsByCategory`) |
| 기록 수정·삭제 진입점 | `ui/detail/DetailScreen.kt` 상단바 ✏️/🗑 (대상 = 현재 보고 있는 `recordId`), `ui/treatment/TreatmentDetailScreen.kt` 편집/삭제. 편집 저장 시 경고 다이얼로그 = `RecordScreen.kt:245`, `TreatmentScreen.kt` |
| 자료 사진: 이슈 단위 첨부 | `data/db/IssueAttachment.kt` (painIssueId 로 이슈에 종속), `data/attachments/AttachmentRepository.kt` |
| 촬영일 vs 추가일 | EXIF `DateTimeOriginal` → `capturedAt`, 없으면 null 이라 UI 가 `createdAt`(추가일)로 폴백. 정렬도 `COALESCE(capturedAt, createdAt) DESC` (`data/db/IssueAttachmentDao.kt`) |
| 사진 무료 1장(이후 1장당 광고) / 20MB 상한 | `FreeLimitsRepository.FREE_ATTACHMENTS_PER_ISSUE`, `AttachmentRepository.MAX_FILE_BYTES` |
| 사진은 백업 미포함 | `.tngd` 는 단일 JSON 통암호화(10MB 상한)라 파일을 담지 못한다. REPLACE_ALL 가져오기는 사진을 삭제하며 `settings_dialog_import_options` 에 경고가 있다 |
| 사진 길게 눌러 삭제 = ✕ | `ui/attachments/AttachmentScreen.kt` (combinedClickable + ✕ 배지). 칩(⊖)과 달리 확인 창을 거친다 — 파일이 영구 삭제이기 때문 |
| 통증 이름 변경·관리창 | `ui/issue/IssueSelectScreen.kt`, `IssueSelectViewModel.renameIssue`: 길게 누르기 → 수정(이름 변경) / 삭제. 상태 변경 UI는 없음 |

## 현재 매뉴얼과 재사용 샘플

- 기준 앱: `app_dev` HEAD `1935b680f9b11d90d6b33bec3848b7f4865e3bc2`, 원격 `cada1b7`을 포함한 merge, `2.4.8 (253)`.
- 매뉴얼 기존 HEAD `d050022` 및 기존 로컬 커밋은 보존한다. 아래 촬영·검증 자료는 v253 갱신 작업 시점의 기록이다.
- `sample-data/README.md`: 한·영 fixture, 날짜 갱신 생성기, 앱 가져오기 가능한 TNGD 및 round-trip 검증.
- `capture-record/README.md`: 촬영 환경·원본·이미지 목록·검수 내역.
- `assets/img/{ko,en}/`: 기존 이미지는 324×720 PNG. 이번 이미지는 1080×2400 원본을 648×1440으로 균일 축소. 웹 표시 폭은 공용 CSS가 제어한다. 기존 README의 “720px 폭”은 잘못된 설명이었다.
- 변경 없는 사진·알림 등 일부 기존 화면은 이전 촬영본을 유지한다. 모든 화면을 v253 촬영본이라고 간주하지 않는다.

## 최신 동작 근거

- `ui/bodymap/BodyMapArea.kt`: 몸 mask 내부 rasterized union, 겹침 중복 제외. 경로 길이 합계 방식이 아님.
- `ui/stats/StatsCalculator.kt`: 날짜별 평균 강도의 평균, 날짜별 최대 범위의 평균, 마지막 유효 바디맵 비교.
- `ui/stats/components/{TrackingTabContent,PeriodComparisonCard,BodyMapChangeCard}.kt`: 무료 현재기간 요약, 이전기간 접근 불가와 기록 없음 구분, %p·유효기록일·중립적 겹침 범례.
- `ui/stats/components/MonthSwingCards.kt`: 최악 대비 지금 / 가장 좋았을 때 대비 최악. 두 카드는 날짜별 최고 강도를 사용하며 일평균 그래프와 기준이 다름.
- `ui/settings/ReportExportDialog.kt`, `data/backup/HtmlReportRepository.kt`: 전체/기간 선택, 무료 범위와 교집합. 지정한 기간이 있을 때 직전 동기간 비교를 구성함.
- `ui/issue/IssueSelectScreen.kt`: 관리창·이름 변경.
- 날짜/시간/기간은 `ui/common`의 `Tongda*PickerDialog` 계열을 공통 사용.

## 로컬 확인

```sh
python3 -m http.server 8873 --bind 127.0.0.1
# http://127.0.0.1:8873/ko/ 또는 /en/
python3 sample-data/generate.py --date 2026-09-09
python3 sample-data/verify.py
```

생성기에는 Python `cryptography`, 검증기에는 `Pillow`가 필요하다. 생성기는 샘플 파일만 갱신하며 앱 데이터나 소스를 수정하지 않는다. 촬영 기준일을 바꾸면 앱에서 새 파일을 가져온 뒤 다시 촬영해야 한다.
