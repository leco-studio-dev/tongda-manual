# v253 매뉴얼 촬영·검증 기록

2026-09-09 KST. 실제 Android 앱 화면이며 화면 위에 통증 표시를 합성하지 않았다. DrawingPath는 샘플 원본에서 앱의 정식 TNGD 가져오기로 저장하고 앱이 직접 렌더했다.

## 기준 / 보존

- 앱 `Dev` branch `app_dev`, HEAD `1935b680f9b11d90d6b33bec3848b7f4865e3bc2`.
- `origin/app_dev` `cada1b7`이 HEAD 조상임을 확인. 이번 Worker에서는 다시 pull하지 않았으며 소스의 staged/unstaged diff가 없다. 기존 미추적 45파일 및 로컬 커밋을 보존했다.
- 매뉴얼 기존 `main` HEAD `d050022`, `origin/main` 대비 기존 1커밋 ahead를 보존. 이번 수정은 미commit·미push·미배포.
- 설치 앱 `studio.leco.tongda`, versionName `2.4.8`, versionCode `253`. 인계받은 `tongda2-v253-debug.apk`를 재사용했고 설치된 버전을 adb로 확인했다. 이번 Worker에서 재빌드·재설치하지 않았다.
- 인계된 빌드는 google-services.json이 없어 일회성 init script로 `processDebugGoogleServices`를 제외해 만든 debug 빌드였다. 프로덕션 설정을 만들지 않았으며 Firebase 사용계측·실결제·광고 송수신 검증을 주장하지 않는다. 인계문의 루트 `.tongda-debug-build.init.gradle`은 작업 시작 시 이미 없었다.

## 환경 / 촬영

- 촬영 전용 AVD `tongda-manual-api35`, `emulator-5554`, Android 15/API 35, 1080×2400.
- 시작 시 AVD가 종료되어 있어 기존 AVD를 재실행했다. wipe-data 또는 실기기·다른 AVD 조작은 하지 않았다.
- 전용 합성 데이터만 교체했다. KO/EN 각각 TNGD 가져오기 → 앱 내보내기 → 앱 파일 재가져오기를 실제 UI에서 성공 확인했다. 기록 ID가 재할당되어도 내용과 연결 관계가 보존되는지 검증했다.
- 프리미엄은 기존 debug/internal-test의 강제 프리미엄 스위치만 사용했다. 구매 상태를 생성하거나 실제 결제하지 않았다. 무료와 프리미엄 화면을 따로 촬영했다.
- UI 선택은 `uiautomator` XML의 text/content-desc/bounds를 ElementTree로 읽어 수행했다. 스크린샷은 `adb exec-out screencap -p` 원본. 캡처 시 실제 표시된 상태바를 유지했다(시계를 09:30으로 고정했다고 주장하지 않음).
- `ko/`, `en/`: 원본 1080×2400 PNG, 언어별 21장(합계 42장).
- `../assets/img/{ko,en}/`: 위 원본을 종횡비 그대로 648×1440으로 축소한 웹 이미지. 합성/재그리기/장식 추가 없음. 기존 변경 없는 324×720 이미지는 유지.
- 웹 표시 폭: 데스크톱 최대 264 CSS px, 모바일 최대 320 CSS px. HTML에 실제 이미지 width/height를 넣어 lazy loading 중 목차 위치가 밀리는 현상도 수정했다.

## 촬영 파일 목록

양쪽 언어 공통, 각 21장. 전체 경로·크기·SHA-256은 `manifest.json`.

- 교체 10장: `01_home.png`, `02_issue_select.png`, `03_record.png`, `04_bodymap.png`, `07_stats_month.png`, `08_stats_trend.png`, `09_stats_day.png`, `11_settings_info.png`, `14_issue_wiggle.png`, `17_detail_actions.png`.
- 추가 11장: `06_detail.png`, `24_stats_notice.png`, `25_tracking_free.png`, `26_tracking_bodymaps.png`, `27_tracking_overlay.png`, `28_issue_rename.png`, `29_date_picker.png`, `30_time_picker.png`, `31_report_period.png`, `32_period_picker.png`, `33_tracking_details.png`.
- `14_issue_wiggle.png`라는 기존 파일명은 링크 보존을 위해 유지하지만 내용은 최신 통증 관리창이다.
- `03_record.png`는 저장된 샘플을 편집하는 화면이며 본문 캡션에도 편집 예시로 표기했다.
- `*-scene-{back,neck,knee}.png`: 세 시나리오의 실제 홈 바디맵을 추가 확인한 원본.
- `*-import-success.png`, `*-roundtrip-success.png`, `en-roundtrip-stats.png`: 실제 복원 결과 증거. 최종 한국어 비교 화면은 `ko-final-compare.png`.

## 검증

- `sample-data/verify.py`: 각 언어 3이슈 / 통증 146 / 처치 55, 782개 다점 획. 모든 획 좌표 body mask 내부, 획별 강도와 기록의 최고 강도 일치, 생성 TNGD 복호화 일치, 앱 자체 export의 내용 일치(재할당 ID와 export 시각 제외).
- `validate_manual.py` / `html-check.json`: 기존 19개 앵커 보존·중복 없음·KO/EN 순서 및 제목 레벨 구조 동일, 기존 링크 모두 보존, 참조 이미지 모두 존재하고 크기 일치. 하루·한달·추적 6장은 모두 다른 파일 내용.
- 모든 새 PNG를 원본 또는 검수 시트로 눈으로 확인했다. 잘린 상세 바디맵 캡처를 다시 촬영했다. `qa/`는 검수용 축소 모음이며 매뉴얼 화면 자체는 합성하지 않았다.
- 실제 로컬 페이지를 연결된 브라우저에서 390×844 및 1280×900으로 렌더했다. 두 언어 본문·새 통계/비교·이름 관리·리포트 기간 화면과 캡션을 확인했다. 이미지 lazy loading에 의한 앵커 이동을 수정 후 재검증했다. `browser-check.json`에 실측 결과를 기록한다.
- 최종 AVD는 한국어, 허리·다리 추적의 최근 30일 / 직전 30일 전후 바디맵 및 범위 흐름 화면을 열어 둔다.

## 다시 촬영

1. `../sample-data/README.md`의 생성기로 기준일 갱신.
2. 앱 언어를 선택한 다음 같은 언어 TNGD를 전용 테스트 AVD에서 가져온다.
3. 통계에서 반드시 분석할 이슈를 선택하고 하루·한달·추적을 별도로 연다.
4. `device.py show`로 XML 상태 확인 후 `device.py tap '정확한 문구'`, `device.py snap 언어/파일명` 사용. adb 경로·전용 serial은 스크립트 상단에 명시되어 있다.
5. 원본을 균일 축소하고 `python3 capture-record/validate_manual.py`, `python3 sample-data/verify.py`를 실행한다. 새 날짜로 바꾸면 앱 export도 다시 받아 비교한다.

## 2026-09-09 후속 QA 보정

- 임시 "업데이트 안내 다시 보기" 기능의 `24_stats_notice.png`와 해당 버튼이 보이는 `11_settings_info.png`는 원본 캡처와 촬영 증거로 보존하되, 현재 KO/EN 매뉴얼 본문에서는 제외했습니다.
- KO/EN `#report`의 설정 진입(전체/기간 → 통증 선택 → 저장)과 상세 진입(현재 통증의 이용 가능한 전체 범위 → 저장, 기간 선택 없음)을 소스와 대조해 구분했습니다. 선택 기간 리포트의 기간 비교 설명은 유지했습니다. `update_manual.py`는 인계 시 현재 트리에 없어 재실행하지 않았습니다.
- 무릎 좌우 메모를 수정한 양언어 샘플로 가져오기·앱 내보내기·재가져오기를 각각 성공했고 `*-import-success.png`, `*-roundtrip-success.png` 4장을 갱신했습니다. `ko-scene-back.png`와 `ko-final-compare.png`도 갱신했습니다. 본문 캡처 42장은 보존했습니다.
- `verify.py`에서 양언어 export 내용 일치, `validate_manual.py`에서 문서 구조·이미지 참조를 재검증했습니다. KO/EN HTML 끝 공백줄을 제거하고 Python 캐시 제외 규칙을 보완했습니다. `git diff --check`도 통과했습니다. 기존 모바일/데스크톱 전체 브라우저 검수는 반복하지 않았습니다.
- 전용 AVD는 한국어 허리·다리 추적의 변동 범위 그래프와 이전/현재 바디맵이 함께 보이는 상태입니다. 앱 소스·빌드·버전 변경, Git 동기화·커밋·푸시, 배포는 하지 않았습니다.
