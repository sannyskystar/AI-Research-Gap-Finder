# import streamlit as st
# import requests
# import re
# from html.parser import HTMLParser


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="AI Research Gap Finder",
#     page_icon="🔬",
#     layout="wide"
# )


# # ============================================================
# # HTML TEXT EXTRACTOR
# # ============================================================

# class ArticleTextExtractor(HTMLParser):

#     def __init__(self):
#         super().__init__()
#         self.text = []

#     def handle_data(self, data):

#         if data.strip():
#             self.text.append(data)


# # ============================================================
# # PAPER ANALYSIS
# # ============================================================

# def analyze_papers(urls):

#     urls = [
#         u.strip()
#         for u in urls.splitlines()
#         if u.strip()
#     ]

#     if not urls:
#         return "❌ Please enter at least one arXiv URL."


#     evidence = {}
#     paper_titles = {}


#     # --------------------------------------------------------
#     # Evidence categories
#     # --------------------------------------------------------

#     keyword_groups = {

#         "artifacts": [
#             "unpleasant artifacts",
#             "introduce artifacts",
#             "artifacts caused by",
#             "twisted lines",
#             "ringing and overshoot"
#         ],

#         "generalization": [
#             "limit the generalization ability",
#             "could not generalize",
#             "out-of-distribution",
#             "unknown and complex degradations"
#         ],

#         "dataset": [
#             "pure synthetic data",
#             "training dataset",
#             "training datasets",
#             "benchmark datasets"
#         ]
#     }


#     # ========================================================
#     # LOAD PAPERS
#     # ========================================================

#     for url in urls:

#         paper_id = (
#             url.rstrip("/")
#             .split("/")[-1]
#             .replace("abs/", "")
#         )


#         try:

#             response = requests.get(
#                 f"https://arxiv.org/html/{paper_id}",
#                 timeout=20
#             )

#         except Exception:

#             continue


#         if response.status_code != 200:
#             continue


#         # ----------------------------------------------------
#         # Extract article text
#         # ----------------------------------------------------

#         parser = ArticleTextExtractor()

#         parser.feed(response.text)

#         text = re.sub(
#             r"\s+",
#             " ",
#             " ".join(parser.text)
#         ).strip()


#         # ----------------------------------------------------
#         # Extract title
#         # ----------------------------------------------------

#         title_match = re.search(
#             r"<title>(.*?)</title>",
#             response.text,
#             re.IGNORECASE | re.DOTALL
#         )


#         if title_match:

#             title = re.sub(
#                 r"\s+",
#                 " ",
#                 title_match.group(1)
#             ).strip()


#             title = re.sub(
#                 r"\s*-\s*arXiv.*$",
#                 "",
#                 title,
#                 flags=re.IGNORECASE
#             )

#         else:

#             title = paper_id


#         paper_titles[paper_id] = title


#         # ----------------------------------------------------
#         # Split into sentences
#         # ----------------------------------------------------

#         sentences = re.split(
#             r"(?<=[.!?])\s+",
#             text
#         )


#         # ----------------------------------------------------
#         # Remove noisy content
#         # ----------------------------------------------------

#         sentences = [

#             s.strip()

#             for s in sentences

#             if (
#                 80 <= len(s.strip()) <= 700

#                 and "http" not in s.lower()

#                 and "@" not in s

#                 and "table " not in s.lower()

#                 and "figure " not in s.lower()

#                 and "affiliation" not in s.lower()

#                 and "footnotetext" not in s.lower()
#             )
#         ]


#         evidence[paper_id] = {}


#         # ----------------------------------------------------
#         # Find evidence
#         # ----------------------------------------------------

#         for group, keywords in keyword_groups.items():

#             matches = []


#             for sentence in sentences:

#                 if any(
#                     keyword in sentence.lower()
#                     for keyword in keywords
#                 ):

#                     matches.append(sentence)


#             evidence[paper_id][group] = list(
#                 dict.fromkeys(matches)
#             )[:2]


#     # ========================================================
#     # ERROR IF NOTHING LOADED
#     # ========================================================

#     if not evidence:

#         return (
#             "❌ No papers could be loaded.\n\n"
#             "Make sure you are using valid public arXiv URLs."
#         )


#     # ========================================================
#     # RESEARCH GAP DEFINITIONS
#     # ========================================================

#     gaps = [

#         (
#             "Artifact / distortion suppression",
#             "artifacts",
#             "High",
#             "Reduce artifacts while preserving perceptual detail."
#         ),

#         (
#             "Robustness to unseen degradations",
#             "generalization",
#             "High",
#             "Improve robustness to unknown and "
#             "out-of-distribution degradation."
#         ),

#         (
#             "Dataset / benchmark dependence",
#             "dataset",
#             "Medium",
#             "Evaluate models across more diverse "
#             "real-world conditions."
#         )
#     ]


#     # ========================================================
#     # BUILD REPORT
#     # ========================================================

#     report = "🔬 RESEARCH GAP REPORT\n"

#     report += "=" * 70 + "\n\n"


#     report += "📚 PAPERS ANALYZED\n"

#     report += "-" * 70 + "\n"


#     for paper_id, title in paper_titles.items():

#         report += f"• {title}\n"


#     report += "\n"

#     report += "=" * 70 + "\n\n"


#     gap_number = 0


#     # ========================================================
#     # GAP ANALYSIS
#     # ========================================================

#     for gap_name, category, confidence, direction in gaps:


#         supporting = [

#             paper

#             for paper, data in evidence.items()

#             if data.get(category)
#         ]


#         # Need at least two papers supporting a candidate gap

#         if len(supporting) < 2:
#             continue


#         non_supporting = [

#             paper

#             for paper in evidence

#             if paper not in supporting
#         ]


#         gap_number += 1


#         report += (
#             f"🔎 GAP {gap_number}: "
#             f"{gap_name}\n"
#         )


#         report += (
#             f"Confidence: {confidence}\n\n"
#         )


#         # ----------------------------------------------------
#         # Supporting papers
#         # ----------------------------------------------------

#         report += "Supporting evidence from:\n"


#         for paper in supporting:

#             report += (
#                 f"  • "
#                 f"{paper_titles.get(paper, paper)}\n"
#             )


#         # ----------------------------------------------------
#         # Non-supporting papers
#         # ----------------------------------------------------

#         if non_supporting:

#             report += (
#                 "\nNo explicit supporting evidence "
#                 "detected in:\n"
#             )


#             for paper in non_supporting:

#                 report += (
#                     f"  • "
#                     f"{paper_titles.get(paper, paper)}\n"
#                 )


#         # ----------------------------------------------------
#         # Research direction
#         # ----------------------------------------------------

#         report += (
#             "\n💡 Potential research direction:\n"
#         )

#         report += (
#             f"  {direction}\n\n"
#         )


#         # ----------------------------------------------------
#         # Evidence
#         # ----------------------------------------------------

#         report += "📌 Evidence excerpts:\n"


#         for paper in supporting:

#             for sentence in evidence[paper][category]:

#                 report += (
#                     f"• [{paper}] "
#                     f"{sentence}\n"
#                 )


#         report += (
#             "\n"
#             + "-" * 70
#             + "\n\n"
#         )


#     # ========================================================
#     # NO GAPS
#     # ========================================================

#     if gap_number == 0:

#         report += (
#             "No strong candidate gaps detected."
#         )


#     # ========================================================
#     # DISCLAIMER
#     # ========================================================

#     report += (
#         "\n⚠️ IMPORTANT\n"
#         "These are evidence-based candidate gaps, "
#         "not proof of research novelty. "
#         "A literature review is still required."
#     )


#     return report


# # ============================================================
# # STREAMLIT UI
# # ============================================================

# st.title("🔬 AI Research Gap Finder")

# st.write(
#     "Compare multiple research papers and identify "
#     "evidence-based candidate research gaps."
# )


# st.markdown(
#     """
# ### 📚 How to use

# 1. Paste **2 or more public arXiv URLs**.
# 2. Put **one URL per line**.
# 3. Click **Analyze Papers**.
# 4. Review the detected research gaps and evidence.
# """
# )


# urls = st.text_area(
#     "📚 arXiv Paper URLs",
#     placeholder=(
#         "https://arxiv.org/abs/1809.00219\n"
#         "https://arxiv.org/abs/2107.10833\n"
#         "https://arxiv.org/abs/2108.10257"
#     ),
#     height=150
# )


# if st.button(
#     "🔬 Analyze Papers",
#     type="primary"
# ):

#     with st.spinner(
#         "Analyzing research papers..."
#     ):

#         report = analyze_papers(urls)


#     st.markdown("## Results")

#     st.text_area(
#         "🔬 Research Gap Analysis",
#         report,
#         height=800
#     )





































































import streamlit as st
import requests
import re
import html
from html.parser import HTMLParser


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Gap Finder",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM UI
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(99,102,241,.13), transparent 28%),
            radial-gradient(circle at 90% 5%, rgba(236,72,153,.10), transparent 25%),
            #0e1117;
    }

    .hero {
        padding: 2.2rem 2.2rem 1.8rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(30,41,59,.95), rgba(49,46,129,.55));
        border: 1px solid rgba(255,255,255,.10);
        box-shadow: 0 16px 45px rgba(0,0,0,.25);
        margin-bottom: 1.4rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.7rem;
        letter-spacing: -0.04em;
    }

    .hero p {
        margin: .65rem 0 0 0;
        color: #cbd5e1;
        font-size: 1.05rem;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: .55rem;
        margin-top: 1rem;
    }

    .badge {
        padding: .38rem .75rem;
        border-radius: 999px;
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(255,255,255,.10);
        color: #e2e8f0;
        font-size: .82rem;
    }

    .panel {
        padding: 1.25rem;
        border-radius: 18px;
        background: rgba(15,23,42,.72);
        border: 1px solid rgba(255,255,255,.08);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: .7rem;
    }

    .result-box {
        padding: 1.25rem;
        border-radius: 18px;
        background: rgba(15,23,42,.82);
        border: 1px solid rgba(129,140,248,.38);
        box-shadow: 0 12px 35px rgba(0,0,0,.20);
        line-height: 1.65;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        color: #e5e7eb;
        font-size: .94rem;
    }

    .metric-card {
        padding: 1rem;
        border-radius: 16px;
        background: rgba(30,41,59,.72);
        border: 1px solid rgba(255,255,255,.08);
        text-align: center;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
    }

    .metric-label {
        color: #94a3b8;
        font-size: .82rem;
    }

    .footer-note {
        margin-top: 1.5rem;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        background: rgba(127,29,29,.16);
        border: 1px solid rgba(248,113,113,.20);
        color: #cbd5e1;
        font-size: .88rem;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 2.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🔬 AI Research Gap Finder</h1>
        <p>
            Compare research papers and surface evidence-based candidate
            research gaps from their literature.
        </p>
        <div class="badge-row">
            <span class="badge">📚 Multi-paper analysis</span>
            <span class="badge">🔎 Evidence extraction</span>
            <span class="badge">📊 Confidence scoring</span>
            <span class="badge">🧠 Computer Vision focused</span>
            <span class="badge">⚡ Live arXiv analysis</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧭 Quick start")

    st.markdown(
        """
        **Best results come from papers in:**

        - Image super-resolution
        - Image restoration
        - Image denoising
        - Image deblurring
        - Blind / real-world restoration
        - JPEG artifact reduction
        - GAN / Transformer restoration
        - Video super-resolution
        """
    )

    st.divider()

    st.markdown("### 🧪 Ready-made test sets")

    sample_sets = {
        "Original 3-paper demo": [
            "https://arxiv.org/abs/1809.00219",
            "https://arxiv.org/abs/2107.10833",
            "https://arxiv.org/abs/2108.10257",
        ],
        "Classic + modern SR": [
            "https://arxiv.org/abs/1511.04587",
            "https://arxiv.org/abs/1707.02921",
            "https://arxiv.org/abs/1807.02758",
        ],
        "Real-world restoration": [
            "https://arxiv.org/abs/2103.14006",
            "https://arxiv.org/abs/2107.10833",
            "https://arxiv.org/abs/2111.09881",
        ],
    }

    selected_set = st.selectbox(
        "Choose a test set",
        list(sample_sets.keys()),
    )

    if st.button("📥 Load test set", use_container_width=True):
        st.session_state["paper_urls"] = "\n".join(
            sample_sets[selected_set]
        )
        st.rerun()

    st.divider()

    st.markdown("### ⚙️ Scope")

    st.caption(
        "This demo is intentionally specialized for image "
        "restoration / low-level computer vision literature. "
        "It is not a general-purpose novelty detector."
    )


# ============================================================
# INPUT AREA
# ============================================================

left, right = st.columns([1.55, 1], gap="large")

with left:

    st.markdown(
        '<div class="section-title">📚 Paper input</div>',
        unsafe_allow_html=True,
    )

    urls = st.text_area(
        "Public arXiv URLs",
        value=st.session_state.get("paper_urls", ""),
        key="paper_urls",
        height=185,
        placeholder=(
            "Paste one public arXiv URL per line\n\n"
            "Example:\n"
            "https://arxiv.org/abs/1809.00219\n"
            "https://arxiv.org/abs/2107.10833\n"
            "https://arxiv.org/abs/2108.10257"
        ),
        label_visibility="collapsed",
    )

    analyze_clicked = st.button(
        "🔬 Analyze Research Gaps",
        type="primary",
        use_container_width=True,
    )


with right:

    st.markdown(
        '<div class="section-title">🎯 What the system looks for</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="panel">
        <b>1. Artifact / distortion suppression</b><br>
        Looks for evidence involving unwanted artifacts, distortions,
        ringing, overshoot and hallucinated structures.
        <br><br>

        <b>2. Robustness to unseen degradations</b><br>
        Looks for distribution shifts, unknown degradations and
        out-of-distribution generalization.
        <br><br>

        <b>3. Dataset / benchmark dependence</b><br>
        Looks for training-data, synthetic-data and benchmark
        dependence signals.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ANALYSIS
# ============================================================

class ArticleTextExtractor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        if data.strip():
            self.text.append(data)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_paper(paper_id):

    response = requests.get(
        f"https://arxiv.org/html/{paper_id}",
        timeout=20,
        headers={
            "User-Agent": "AI-Research-Gap-Finder/1.0"
        },
    )

    response.raise_for_status()

    return response.text


def extract_title(raw_html, paper_id):

    title_match = re.search(
        r"<title>(.*?)</title>",
        raw_html,
        re.IGNORECASE | re.DOTALL,
    )

    if not title_match:
        return paper_id

    title = re.sub(
        r"\s+",
        " ",
        title_match.group(1),
    ).strip()

    title = re.sub(
        r"\s*-\s*arXiv.*$",
        "",
        title,
        flags=re.IGNORECASE,
    )

    return title


def analyze_papers(urls):

    urls = [
        u.strip()
        for u in urls.splitlines()
        if u.strip()
    ]

    if not urls:
        return (
            "❌ Please enter at least one public arXiv URL.",
            0,
            0,
        )

    evidence = {}
    paper_titles = {}

    keyword_groups = {
        "artifacts": [
            "unpleasant artifacts",
            "introduce artifacts",
            "artifacts caused by",
            "artifacts due to",
            "twisted lines",
            "ringing and overshoot",
        ],
        "generalization": [
            "limit the generalization ability",
            "could not generalize",
            "out-of-distribution",
            "unknown and complex degradations",
        ],
        "dataset": [
            "pure synthetic data",
            "training dataset",
            "training datasets",
            "benchmark datasets",
        ],
    }

    for url in urls:

        paper_id = (
            url.rstrip("/")
            .split("/")[-1]
            .replace("abs/", "")
        )

        try:
            raw_html = fetch_paper(paper_id)

        except Exception:
            continue

        parser = ArticleTextExtractor()
        parser.feed(raw_html)

        text = re.sub(
            r"\s+",
            " ",
            " ".join(parser.text),
        ).strip()

        paper_titles[paper_id] = extract_title(
            raw_html,
            paper_id,
        )

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        sentences = [
            s.strip()
            for s in sentences
            if (
                80 <= len(s.strip()) <= 700
                and "http" not in s.lower()
                and "@" not in s
                and "table " not in s.lower()
                and "figure " not in s.lower()
                and "affiliation" not in s.lower()
                and "footnotetext" not in s.lower()
            )
        ]

        evidence[paper_id] = {}

        for group, keywords in keyword_groups.items():

            matches = [
                sentence
                for sentence in sentences
                if any(
                    keyword in sentence.lower()
                    for keyword in keywords
                )
            ]

            evidence[paper_id][group] = list(
                dict.fromkeys(matches)
            )[:2]

    if not evidence:
        return (
            "❌ No papers could be loaded.\n\n"
            "Make sure the URLs point to public arXiv papers "
            "with an available HTML version.",
            0,
            0,
        )

    gaps = [
        (
            "Artifact / distortion suppression",
            "artifacts",
            "High",
            "Reduce artifacts while preserving perceptual detail.",
        ),
        (
            "Robustness to unseen degradations",
            "generalization",
            "High",
            "Improve robustness to unknown and "
            "out-of-distribution degradation.",
        ),
        (
            "Dataset / benchmark dependence",
            "dataset",
            "Medium",
            "Evaluate models across more diverse "
            "real-world conditions.",
        ),
    ]

    report = "🔬 RESEARCH GAP REPORT\n"
    report += "=" * 70 + "\n\n"

    report += "📚 PAPERS ANALYZED\n"
    report += "-" * 70 + "\n"

    for paper_id, title in paper_titles.items():
        report += f"• {title}\n"

    report += "\n" + "=" * 70 + "\n\n"

    gap_number = 0

    for gap_name, category, confidence, direction in gaps:

        supporting = [
            paper
            for paper, data in evidence.items()
            if data.get(category)
        ]

        if len(supporting) < 2:
            continue

        non_supporting = [
            paper
            for paper in evidence
            if paper not in supporting
        ]

        gap_number += 1

        report += (
            f"🔎 GAP {gap_number}: {gap_name}\n"
        )

        report += (
            f"Confidence: {confidence}\n\n"
        )

        report += "Supporting evidence from:\n"

        for paper in supporting:
            report += (
                f"  • {paper_titles.get(paper, paper)}\n"
            )

        if non_supporting:
            report += (
                "\nNo explicit supporting evidence detected in:\n"
            )

            for paper in non_supporting:
                report += (
                    f"  • {paper_titles.get(paper, paper)}\n"
                )

        report += (
            "\n💡 Potential research direction:\n"
            f"  {direction}\n\n"
        )

        report += "📌 Evidence excerpts:\n"

        for paper in supporting:

            for sentence in evidence[paper][category]:

                report += (
                    f"• [{paper}] {sentence}\n"
                )

        report += "\n" + "-" * 70 + "\n\n"

    if gap_number == 0:
        report += "No strong candidate gaps detected."

    report += (
        "\n⚠️ IMPORTANT\n"
        "These are evidence-based candidate gaps, "
        "not proof of research novelty. "
        "A literature review is still required."
    )

    return report, len(evidence), gap_number


# ============================================================
# RUN BUTTON
# ============================================================

if analyze_clicked:

    with st.spinner(
        "🔎 Fetching papers and comparing evidence..."
    ):

        report, paper_count, gap_count = analyze_papers(urls)

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Analysis summary</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{paper_count}</div>
                <div class="metric-label">Papers analyzed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{gap_count}</div>
                <div class="metric-label">Candidate gaps</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        status = "Evidence found" if gap_count else "No strong gaps"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{"🟢" if gap_count else "🟡"}</div>
                <div class="metric-label">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🔬 Research Gap Analysis")

    safe_report = html.escape(report).replace("\n", "<br>")

    st.markdown(
        f'<div class="result-box">{safe_report}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
        ⚠️ <b>Research disclaimer:</b>
        This tool identifies evidence-based candidate research gaps
        from predefined literature signals. It does not establish
        research novelty or replace a systematic literature review.
    </div>
    """,
    unsafe_allow_html=True,
)
