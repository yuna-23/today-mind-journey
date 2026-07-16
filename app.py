from __future__ import annotations

from datetime import datetime
import random

import pandas as pd
import streamlit as st


# =========================================================
# 페이지 기본 설정
# =========================================================

st.set_page_config(
    page_title="오늘의 마음 여행",
    page_icon="🌈",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# 화면 스타일
# =========================================================

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #59636e;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .step-box {
        background: #f7f9fc;
        border: 1px solid #e3e8ef;
        border-radius: 18px;
        padding: 1.1rem 1.3rem;
        margin: 1rem 0 1.4rem 0;
    }

    .emotion-result {
        background: linear-gradient(
            135deg,
            #fff7df 0%,
            #f7f2ff 100%
        );
        border: 1px solid #eadff7;
        border-radius: 22px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }

    .mission-card {
        background: #eef8f2;
        border: 2px solid #b7dec5;
        border-radius: 22px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }

    .mission-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #245c38;
        margin-bottom: 0.7rem;
    }

    .mission-text {
        font-size: 1.3rem;
        font-weight: 700;
        line-height: 1.6;
    }

    .small-guide {
        color: #6b7280;
        font-size: 0.93rem;
    }

    div[data-testid="stButton"] > button {
        border-radius: 14px;
        min-height: 3rem;
        font-weight: 700;
    }

    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 14px;
        min-height: 3rem;
        font-weight: 700;
    }

    div[data-testid="stRadio"] label {
        font-size: 1.03rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 앱에서 사용할 자료
# =========================================================

EMOTIONS = {
    "기뻐요": {
        "emoji": "😊",
        "message": "기쁜 마음을 알아차렸군요. 좋은 마음을 주변과 나누어 보세요.",
    },
    "편안해요": {
        "emoji": "😌",
        "message": "마음이 편안하군요. 지금의 안정된 느낌을 천천히 느껴 보세요.",
    },
    "설레요": {
        "emoji": "🤗",
        "message": "기대되고 설레는 마음이 있군요. 무엇을 기다리는지 생각해 보세요.",
    },
    "속상해요": {
        "emoji": "😢",
        "message": "속상한 마음도 소중한 마음입니다. 마음을 말로 표현해 보세요.",
    },
    "화나요": {
        "emoji": "😠",
        "message": "화가 난 것을 알아차린 것이 첫걸음입니다. 잠시 멈추고 숨을 쉬어 보세요.",
    },
    "걱정돼요": {
        "emoji": "😟",
        "message": "걱정되는 일이 있군요. 혼자 해결하기 어렵다면 믿을 만한 어른에게 알려 주세요.",
    },
    "피곤해요": {
        "emoji": "😴",
        "message": "몸과 마음에 쉼이 필요하다는 신호일 수 있어요.",
    },
    "잘 모르겠어요": {
        "emoji": "🤔",
        "message": "마음을 바로 알기 어려울 수도 있어요. 천천히 몸의 느낌부터 살펴보세요.",
    },
}

REASONS = [
    "친구와의 일",
    "공부나 과제",
    "가족과의 일",
    "학교생활",
    "건강이나 피로",
    "기대되는 일",
    "특별한 이유 없이",
    "직접 적을래요",
]

MISSIONS_BY_EMOTION = {
    "기뻐요": [
        "오늘 고마운 사람 한 명에게 마음을 표현해 보세요.",
        "친구에게 따뜻한 말 한마디를 건네 보세요.",
        "기뻤던 일을 한 문장으로 기록해 보세요.",
    ],
    "편안해요": [
        "눈을 감고 천천히 세 번 숨을 쉬어 보세요.",
        "지금 편안하게 느껴지는 것을 세 가지 찾아보세요.",
        "오늘도 마음을 편안하게 지키기 위해 할 일을 하나 정해 보세요.",
    ],
    "설레요": [
        "기대하는 일이 무엇인지 한 문장으로 적어 보세요.",
        "기대하는 일을 잘 준비하기 위한 작은 행동 하나를 해 보세요.",
        "설레는 마음을 친구나 가족에게 이야기해 보세요.",
    ],
    "속상해요": [
        "‘나는 ___해서 속상했어.’라고 마음을 문장으로 표현해 보세요.",
        "믿을 만한 친구나 어른에게 속상한 일을 이야기해 보세요.",
        "나에게 ‘그럴 수도 있어. 괜찮아.’라고 말해 주세요.",
    ],
    "화나요": [
        "손을 배 위에 올리고 천천히 다섯 번 숨을 쉬어 보세요.",
        "바로 행동하기 전에 마음속으로 열까지 세어 보세요.",
        "‘나는 ___해서 화가 났어.’라고 차분하게 표현해 보세요.",
    ],
    "걱정돼요": [
        "걱정되는 일과 내가 할 수 있는 일을 하나씩 나누어 적어 보세요.",
        "도움을 요청할 수 있는 어른 한 명을 떠올려 보세요.",
        "지금 할 수 있는 가장 작은 행동 하나를 시작해 보세요.",
    ],
    "피곤해요": [
        "물 한 잔을 마시고 어깨와 목을 가볍게 움직여 보세요.",
        "오늘 꼭 해야 할 일과 미뤄도 되는 일을 나누어 보세요.",
        "잠시 화면에서 눈을 떼고 먼 곳을 바라보세요.",
    ],
    "잘 모르겠어요": [
        "지금 몸에서 가장 먼저 느껴지는 느낌을 찾아보세요.",
        "오늘 있었던 일을 아침부터 차례대로 떠올려 보세요.",
        "‘지금 내 마음은 날씨로 말하면 ___ 같아.’라고 표현해 보세요.",
    ],
}


# =========================================================
# 세션 상태 초기화
# =========================================================

def initialize_state() -> None:
    defaults = {
        "current_step": 1,
        "emotion": None,
        "reason": None,
        "custom_reason": "",
        "reflection": "",
        "mission": None,
        "records": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def restart_journey() -> None:
    st.session_state.current_step = 1
    st.session_state.emotion = None
    st.session_state.reason = None
    st.session_state.custom_reason = ""
    st.session_state.reflection = ""
    st.session_state.mission = None


def choose_new_mission() -> None:
    emotion = st.session_state.emotion

    if emotion:
        possible_missions = MISSIONS_BY_EMOTION[emotion]
        current_mission = st.session_state.mission

        new_candidates = [
            mission
            for mission in possible_missions
            if mission != current_mission
        ]

        st.session_state.mission = random.choice(
            new_candidates or possible_missions
        )


initialize_state()


# =========================================================
# 공통 화면
# =========================================================

st.markdown(
    '<div class="main-title">🌈 오늘의 마음 여행</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        내 마음을 알아차리고, 표현하고, 돌보는 짧은 여행을 시작해요.
    </div>
    """,
    unsafe_allow_html=True,
)

progress_value = st.session_state.current_step / 4
st.progress(progress_value)

st.caption(
    f"마음 여행 {st.session_state.current_step}단계 / 4단계"
)


# =========================================================
# 1단계: 감정 선택
# =========================================================

if st.session_state.current_step == 1:
    st.markdown(
        """
        <div class="step-box">
            <b>1단계 · 지금 내 마음은 어떤가요?</b><br>
            정답은 없어요. 지금 나와 가장 가까운 마음을 골라 보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    emotion_options = [
        f"{details['emoji']} {emotion}"
        for emotion, details in EMOTIONS.items()
    ]

    selected_emotion_label = st.radio(
        "지금 내 마음과 가장 가까운 것을 선택하세요.",
        emotion_options,
        index=None,
        horizontal=True,
        key="emotion_radio",
    )

    if selected_emotion_label:
        selected_emotion = selected_emotion_label.split(
            " ",
            maxsplit=1,
        )[1]

        details = EMOTIONS[selected_emotion]

        st.markdown(
            f"""
            <div class="emotion-result">
                <div style="font-size:3rem;">
                    {details["emoji"]}
                </div>
                <div style="font-size:1.35rem; font-weight:800;">
                    나는 지금 {selected_emotion}
                </div>
                <div style="margin-top:0.7rem;">
                    {details["message"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "다음으로",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.emotion = selected_emotion
            st.session_state.current_step = 2
            st.rerun()


# =========================================================
# 2단계: 이유 살펴보기
# =========================================================

elif st.session_state.current_step == 2:
    selected_emotion = st.session_state.emotion
    emotion_details = EMOTIONS[selected_emotion]

    st.markdown(
        f"""
        <div class="step-box">
            <b>2단계 · 왜 이런 마음이 들었을까요?</b><br>
            {emotion_details["emoji"]}
            <b>{selected_emotion}</b> 마음이 든 까닭을 떠올려 보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("reason_form"):
        selected_reason = st.radio(
            "가장 가까운 까닭을 선택하세요.",
            REASONS,
            index=None,
        )

        custom_reason = ""

        if selected_reason == "직접 적을래요":
            custom_reason = st.text_input(
                "어떤 일이 있었나요?",
                placeholder="짧게 적어도 괜찮아요.",
                max_chars=80,
            )

        reflection = st.text_area(
            "오늘 있었던 일을 한 줄로 적어 보세요.",
            placeholder=(
                "예: 발표할 때 친구들이 잘 들어줘서 기뻤어요."
            ),
            max_chars=150,
            height=110,
        )

        submitted = st.form_submit_button(
            "다음으로",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if selected_reason is None:
            st.warning("마음이 든 까닭을 하나 선택해 주세요.")

        elif selected_reason == "직접 적을래요" and not custom_reason.strip():
            st.warning("마음이 든 까닭을 짧게 적어 주세요.")

        elif not reflection.strip():
            st.warning("오늘 있었던 일을 한 줄로 적어 주세요.")

        else:
            st.session_state.reason = (
                custom_reason.strip()
                if selected_reason == "직접 적을래요"
                else selected_reason
            )
            st.session_state.reflection = reflection.strip()
            st.session_state.mission = random.choice(
                MISSIONS_BY_EMOTION[selected_emotion]
            )
            st.session_state.current_step = 3
            st.rerun()

    if st.button(
        "이전 단계로",
        use_container_width=True,
    ):
        st.session_state.current_step = 1
        st.rerun()


# =========================================================
# 3단계: 실천 카드
# =========================================================

elif st.session_state.current_step == 3:
    selected_emotion = st.session_state.emotion
    emotion_details = EMOTIONS[selected_emotion]

    st.markdown(
        """
        <div class="step-box">
            <b>3단계 · 오늘의 마음 돌봄 카드</b><br>
            지금 내 마음을 돌보기 위한 작은 행동을 실천해 보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="mission-card">
            <div style="font-size:2.5rem;">
                {emotion_details["emoji"]}
            </div>
            <div class="mission-title">
                오늘의 마음 돌봄 미션
            </div>
            <div class="mission-text">
                {st.session_state.mission}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "다른 카드 뽑기",
            use_container_width=True,
        ):
            choose_new_mission()
            st.rerun()

    with col2:
        if st.button(
            "이 카드로 실천할래요",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.current_step = 4
            st.rerun()

    if st.button(
        "이전 단계로",
        use_container_width=True,
    ):
        st.session_state.current_step = 2
        st.rerun()


# =========================================================
# 4단계: 여행 완료 및 기록
# =========================================================

else:
    emotion = st.session_state.emotion
    emotion_details = EMOTIONS[emotion]

    st.balloons()

    st.markdown(
        """
        <div class="step-box">
            <b>4단계 · 오늘의 마음 여행 완료!</b><br>
            내 마음을 알아차리고 돌보는 연습을 잘 마쳤어요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="emotion-result">
            <div style="font-size:3rem;">
                {emotion_details["emoji"]}
            </div>
            <div style="font-size:1.4rem; font-weight:800;">
                오늘 나는 ‘{emotion}’ 마음을 느꼈어요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    summary_data = {
        "오늘의 마음": f"{emotion_details['emoji']} {emotion}",
        "마음이 든 까닭": st.session_state.reason,
        "오늘 있었던 일": st.session_state.reflection,
        "마음 돌봄 미션": st.session_state.mission,
    }

    for title, content in summary_data.items():
        st.markdown(f"**{title}**")
        st.write(content)

    record_already_saved = any(
        record.get("session_id")
        == st.session_state.get("active_record_id")
        for record in st.session_state.records
    )

    if not record_already_saved:
        record_id = datetime.now().isoformat()

        st.session_state.active_record_id = record_id
        st.session_state.records.append(
            {
                "session_id": record_id,
                "기록 시각": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "감정": emotion,
                "까닭": st.session_state.reason,
                "오늘의 한 줄": st.session_state.reflection,
                "실천 미션": st.session_state.mission,
            }
        )

    st.success(
        "마음을 알아차리는 연습을 한 것만으로도 충분히 잘했어요."
    )

    if st.button(
        "새로운 마음 여행 시작하기",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.active_record_id = None
        restart_journey()
        st.rerun()


# =========================================================
# 사이드바: 이용 안내와 현재 세션 기록
# =========================================================

with st.sidebar:
    st.header("🌿 이용 안내")

    st.write(
        """
        이 앱은 자신의 감정을 알아차리고 표현하는 연습을 돕습니다.

        힘들거나 위험한 일이 있다면 앱에만 적지 말고,  
        반드시 부모님이나 선생님 등 믿을 만한 어른에게 알려 주세요.
        """
    )

    st.divider()

    st.subheader("현재 접속 기록")

    if st.session_state.records:
        records_df = pd.DataFrame(
            st.session_state.records
        ).drop(columns=["session_id"])

        st.dataframe(
            records_df,
            hide_index=True,
            use_container_width=True,
        )

        csv_data = records_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "내 기록 내려받기",
            data=csv_data,
            file_name="오늘의_마음_여행_기록.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if st.button(
            "현재 기록 모두 지우기",
            use_container_width=True,
        ):
            st.session_state.records = []
            st.session_state.active_record_id = None
            st.rerun()

    else:
        st.caption(
            "아직 저장된 마음 여행 기록이 없습니다."
        )
