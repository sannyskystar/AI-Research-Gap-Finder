import streamlit as st
import requests
import re
from html.parser import HTMLParser


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Gap Finder",
    page_icon="🔬",
    layout="wide"
)


# ============================================================
# HTML TEXT EXTRACTOR
# ============================================================

class ArticleTextExtractor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):

        if data.strip():
            self.text.append(data)


# ============================================================
# PAPER ANALYSIS
# ============================================================

def analyze_papers(urls):

    urls = [
        u.strip()
        for u in urls.splitlines()
        if u.strip()
    ]

    if not urls:
        return "❌ Please enter at least one arXiv URL."


    evidence = {}
    paper_titles = {}


    # --------------------------------------------------------
    # Evidence categories
    # --------------------------------------------------------

    keyword_groups = {

        "artifacts": [
            "unpleasant artifacts",
            "introduce artifacts",
            "artifacts caused by",
            "twisted lines",
            "ringing and overshoot"
        ],

        "generalization": [
            "limit the generalization ability",
            "could not generalize",
            "out-of-distribution",
            "unknown and complex degradations"
        ],

        "dataset": [
            "pure synthetic data",
            "training dataset",
            "training datasets",
            "benchmark datasets"
        ]
    }


    # ========================================================
    # LOAD PAPERS
    # ========================================================

    for url in urls:

        paper_id = (
            url.rstrip("/")
            .split("/")[-1]
            .replace("abs/", "")
        )


        try:

            response = requests.get(
                f"https://arxiv.org/html/{paper_id}",
                timeout=20
            )

        except Exception:

            continue


        if response.status_code != 200:
            continue


        # ----------------------------------------------------
        # Extract article text
        # ----------------------------------------------------

        parser = ArticleTextExtractor()

        parser.feed(response.text)

        text = re.sub(
            r"\s+",
            " ",
            " ".join(parser.text)
        ).strip()


        # ----------------------------------------------------
        # Extract title
        # ----------------------------------------------------

        title_match = re.search(
            r"<title>(.*?)</title>",
            response.text,
            re.IGNORECASE | re.DOTALL
        )


        if title_match:

            title = re.sub(
                r"\s+",
                " ",
                title_match.group(1)
            ).strip()


            title = re.sub(
                r"\s*-\s*arXiv.*$",
                "",
                title,
                flags=re.IGNORECASE
            )

        else:

            title = paper_id


        paper_titles[paper_id] = title


        # ----------------------------------------------------
        # Split into sentences
        # ----------------------------------------------------

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )


        # ----------------------------------------------------
        # Remove noisy content
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # Find evidence
        # ----------------------------------------------------

        for group, keywords in keyword_groups.items():

            matches = []


            for sentence in sentences:

                if any(
                    keyword in sentence.lower()
                    for keyword in keywords
                ):

                    matches.append(sentence)


            evidence[paper_id][group] = list(
                dict.fromkeys(matches)
            )[:2]


    # ========================================================
    # ERROR IF NOTHING LOADED
    # ========================================================

    if not evidence:

        return (
            "❌ No papers could be loaded.\n\n"
            "Make sure you are using valid public arXiv URLs."
        )


    # ========================================================
    # RESEARCH GAP DEFINITIONS
    # ========================================================

    gaps = [

        (
            "Artifact / distortion suppression",
            "artifacts",
            "High",
            "Reduce artifacts while preserving perceptual detail."
        ),

        (
            "Robustness to unseen degradations",
            "generalization",
            "High",
            "Improve robustness to unknown and "
            "out-of-distribution degradation."
        ),

        (
            "Dataset / benchmark dependence",
            "dataset",
            "Medium",
            "Evaluate models across more diverse "
            "real-world conditions."
        )
    ]


    # ========================================================
    # BUILD REPORT
    # ========================================================

    report = "🔬 RESEARCH GAP REPORT\n"

    report += "=" * 70 + "\n\n"


    report += "📚 PAPERS ANALYZED\n"

    report += "-" * 70 + "\n"


    for paper_id, title in paper_titles.items():

        report += f"• {title}\n"


    report += "\n"

    report += "=" * 70 + "\n\n"


    gap_number = 0


    # ========================================================
    # GAP ANALYSIS
    # ========================================================

    for gap_name, category, confidence, direction in gaps:


        supporting = [

            paper

            for paper, data in evidence.items()

            if data.get(category)
        ]


        # Need at least two papers supporting a candidate gap

        if len(supporting) < 2:
            continue


        non_supporting = [

            paper

            for paper in evidence

            if paper not in supporting
        ]


        gap_number += 1


        report += (
            f"🔎 GAP {gap_number}: "
            f"{gap_name}\n"
        )


        report += (
            f"Confidence: {confidence}\n\n"
        )


        # ----------------------------------------------------
        # Supporting papers
        # ----------------------------------------------------

        report += "Supporting evidence from:\n"


        for paper in supporting:

            report += (
                f"  • "
                f"{paper_titles.get(paper, paper)}\n"
            )


        # ----------------------------------------------------
        # Non-supporting papers
        # ----------------------------------------------------

        if non_supporting:

            report += (
                "\nNo explicit supporting evidence "
                "detected in:\n"
            )


            for paper in non_supporting:

                report += (
                    f"  • "
                    f"{paper_titles.get(paper, paper)}\n"
                )


        # ----------------------------------------------------
        # Research direction
        # ----------------------------------------------------

        report += (
            "\n💡 Potential research direction:\n"
        )

        report += (
            f"  {direction}\n\n"
        )


        # ----------------------------------------------------
        # Evidence
        # ----------------------------------------------------

        report += "📌 Evidence excerpts:\n"


        for paper in supporting:

            for sentence in evidence[paper][category]:

                report += (
                    f"• [{paper}] "
                    f"{sentence}\n"
                )


        report += (
            "\n"
            + "-" * 70
            + "\n\n"
        )


    # ========================================================
    # NO GAPS
    # ========================================================

    if gap_number == 0:

        report += (
            "No strong candidate gaps detected."
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    report += (
        "\n⚠️ IMPORTANT\n"
        "These are evidence-based candidate gaps, "
        "not proof of research novelty. "
        "A literature review is still required."
    )


    return report


# ============================================================
# STREAMLIT UI
# ============================================================

st.title("🔬 AI Research Gap Finder")

st.write(
    "Compare multiple research papers and identify "
    "evidence-based candidate research gaps."
)


st.markdown(
    """
### 📚 How to use

1. Paste **2 or more public arXiv URLs**.
2. Put **one URL per line**.
3. Click **Analyze Papers**.
4. Review the detected research gaps and evidence.
"""
)


urls = st.text_area(
    "📚 arXiv Paper URLs",
    placeholder=(
        "https://arxiv.org/abs/1809.00219\n"
        "https://arxiv.org/abs/2107.10833\n"
        "https://arxiv.org/abs/2108.10257"
    ),
    height=150
)


if st.button(
    "🔬 Analyze Papers",
    type="primary"
):

    with st.spinner(
        "Analyzing research papers..."
    ):

        report = analyze_papers(urls)


    st.markdown("## Results")

    st.text_area(
        "🔬 Research Gap Analysis",
        report,
        height=800
    )
