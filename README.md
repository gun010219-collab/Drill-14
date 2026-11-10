# Drill-14

교수님 [LEC16_Time](https://github.com/unreal-class/2026-2DGP/tree/398fbcbe15ca80566b35be9605e54ea769e02c32/Labs/LEC16_Time)을 기초로 구현했다. 원본 파일과 리소스를 함께 보존했으며 출처는 `UPSTREAM.txt`에 기록했다.

실행: `python -m pip install -r requirements.txt` 후 `python main.py`. 창 크기는 1600×600이며 Esc 또는 창 닫기로 종료한다.

`Bird` 10개만 `game_world`의 레이어 1에 등록한다. 높이·초기 위치·방향·애니메이션 위상을 분산한다. 초기화 시 월드를 비우고 종료 시 목록과 월드를 정리한다. 원본 Boy/Grass 코드는 보존하지만 실행 장면에는 등록하지 않는다.

원본 `bird_animation.png`는 918×506이며 오른쪽을 보는 새 14프레임이 위에서 아래로 5·5·4개 배치되어 있다. 투명 픽셀 경계를 조사한 결과 열별 실제 픽셀 범위는 x=34–179, 216–361, 376–543, 546–725, 728–909이고, 행별 범위는 y=1–143, 216–339, 370–499(위쪽 원점)이다. 따라서 단순히 높이를 3등분하면 두 번째 행의 날개 끝을 자를 수 있다. 투명 여백 안에서 열 경계 0/182/364/546/728/918, 행 경계 0/170/340/506으로 자른다. 마지막 행의 빈 다섯 번째 칸은 제외한다. pico2d의 아래쪽 원점으로 `bottom = 506 - row_end`를 계산한다.

`game_framework`는 `time.perf_counter()`로 매 루프의 실제 경과 시간을 `frame_time`에 저장한다. 애니메이션은 `(frame + 14 * frame_time) % 14`로 계산하며 1초에 한 주기를 재생한다. 이동 속도는 200픽셀/초다. 표시 크기는 110×102이고 중심 x는 55–1545 안에서 왕복한다. 왕복 경로를 펼친 위상에 이동 거리를 더하고 나머지 연산 후 반사하여 큰 시간 간격에서도 초과 거리를 보존한다. 원본은 오른쪽을 보므로 왼쪽 비행 시에만 수평 반전한다.

검증 명령:

```text
python -m compileall -q .
python -m unittest -v
```

단위 테스트는 이미지를 Mock으로 대체하여 시간 분할 독립성, 양끝 반사, 속도, 14프레임과 방향별 그리기, 정확히 10개 객체 등록 및 정리를 검사한다. 실제 이미지 로딩과 렌더링은 별도의 SDL smoke 실행으로 확인한다.


## Final submission verification (2026-11-10)

Run `python -m compileall -q .`, `python -m unittest -v`, and
`python verify_submission.py` from the project directory.
All three checks passed: four unit tests, plus 60 real SDL update/render
frames with exactly ten birds, all 14 animation indices, both flight
directions, onscreen bounds and shutdown cleanup. The validation script
also checks required Git-tracked files and the original image blob hash
`8c19f4108af91c6497c332d408a756e83b52d5ef`.
No prolonged visual inspection was performed.

The initial implementation was already committed and pushed as one commit
before the request for five development commits arrived. Its history is
preserved. Later commits contain actual validation and documentation work;
they do not reconstruct the five original development stages. The minimum
five-stage development-history requirement remains unmet.
