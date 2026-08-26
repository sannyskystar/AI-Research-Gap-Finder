# 🔬 AI Research Gap Finder

A lightweight research-literature analysis demo that compares multiple public arXiv papers and identifies **evidence-based candidate research gaps**.

> **Important:** This is a research/portfolio prototype, not an automated novelty detector. Detected gaps are candidate directions based on textual evidence and should be validated through a proper literature review.

## 🚀 Live Demo

Run the project on **Streamlit Community Cloud**:

https://share.streamlit.io/

The app can be deployed directly from this GitHub repository.

---

## ✨ What it does

The user provides multiple public arXiv paper URLs. The system:

1. Fetches the papers from arXiv's public HTML pages.
2. Extracts article text and paper titles.
3. Searches the literature for predefined evidence signals.
4. Compares those signals across papers.
5. Identifies candidate research gaps when at least two papers provide supporting evidence.
6. Reports:
   - candidate research gap
   - confidence level
   - supporting papers
   - non-supporting papers
   - evidence excerpts
   - potential research direction

### Current candidate gap categories

- **Artifact / distortion suppression**
- **Robustness to unseen degradations**
- **Dataset / benchmark dependence**

---

## 🎯 Intended domain

The current implementation is intentionally specialized for:

- Computer Vision
- Low-Level Vision
- Image Restoration
- Image Super-Resolution
- Blind / Real-World Super-Resolution
- Image Denoising
- Image Deblurring
- JPEG Compression Artifact Reduction
- GAN-based Image Restoration
- Transformer-based Image Restoration
- Video Super-Resolution / Restoration

It is **not designed as a general-purpose research-gap detector for arbitrary academic disciplines**.

For example, physics, economics, chemistry, or unrelated medical papers may correctly produce:

> No strong candidate gaps detected.

That behavior is preferable to inventing unsupported research gaps.

---

## 🧪 Recommended paper topics

For the best live-demo results, try papers containing terms/concepts such as:

- super-resolution
- image restoration
- real-world degradation
- blind super-resolution
- image artifacts
- distortion
- hallucination
- ringing
- overshoot
- generalization
- out-of-distribution
- unknown degradation
- synthetic data
- training dataset
- benchmark datasets
- denoising
- deblurring
- JPEG artifacts
- perceptual quality
- GAN restoration
- Transformer restoration

### Useful paper sections

The detector is especially likely to find useful evidence when papers contain discussion in:

- Introduction
- Related Work
- Method / Methodology
- Experiments
- Ablation Study
- Limitations
- Future Work
- Generalization
- Dataset / Training Data
- Benchmark / Evaluation

---

# 🧪 Ready-to-test arXiv papers

Paste **2 or more** of these into the demo.

## Classical / Single-Image Super-Resolution

1. SRCNN — Learning a Deep Convolutional Network for Image Super-Resolution  
   https://arxiv.org/abs/1501.00092

2. VDSR — Accurate Image Super-Resolution Using Very Deep Convolutional Networks  
   https://arxiv.org/abs/1511.04587

3. SRGAN — Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network  
   https://arxiv.org/abs/1609.04802

4. LapSRN — Deep Laplacian Pyramid Networks for Fast and Accurate Super-Resolution  
   https://arxiv.org/abs/1704.03915

5. EDSR — Enhanced Deep Residual Networks for Single Image Super-Resolution  
   https://arxiv.org/abs/1707.02921

6. RDN — Residual Dense Network for Image Super-Resolution  
   https://arxiv.org/abs/1802.08797

7. DBPN — Deep Back-Projection Networks for Super-Resolution  
   https://arxiv.org/abs/1803.02735

8. RCAN — Image Super-Resolution Using Very Deep Residual Channel Attention Networks  
   https://arxiv.org/abs/1807.02758

## GAN / Real-World / Blind Restoration

9. ESRGAN — Enhanced Super-Resolution Generative Adversarial Networks  
   https://arxiv.org/abs/1809.00219

10. BSRGAN — Designing a Practical Degradation Model for Deep Blind Image Super-Resolution  
    https://arxiv.org/abs/2103.14006

11. Real-ESRGAN — Training Real-World Blind Super-Resolution with Pure Synthetic Data  
    https://arxiv.org/abs/2107.10833

## Transformer / General Image Restoration

12. IPT — Pre-Trained Image Processing Transformer  
    https://arxiv.org/abs/2012.00364

13. SwinIR — Image Restoration Using Swin Transformer  
    https://arxiv.org/abs/2108.10257

14. Uformer — A General U-Shaped Transformer for Image Restoration  
    https://arxiv.org/abs/2106.03106

15. Restormer — Efficient Transformer for High-Resolution Image Restoration  
    https://arxiv.org/abs/2111.09881

16. NAFNet — Simple Baselines for Image Restoration  
    https://arxiv.org/abs/2204.04676

17. HAT — Hybrid Attention Transformer for Image Restoration  
    https://arxiv.org/abs/2309.05239

## Video Super-Resolution / Restoration

18. EDVR — Video Restoration with Enhanced Deformable Convolutional Networks  
    https://arxiv.org/abs/1905.02716

19. SOF-VSR — Deep Video Super-Resolution using HR Optical Flow Estimation  
    https://arxiv.org/abs/2001.02129

20. BasicVSR — The Search for Essential Components in Video Super-Resolution and Beyond  
    https://arxiv.org/abs/2012.02181

## Other Related Restoration Papers

21. MPRNet — MPRNet: Multi-Stage Progressive Image Restoration  
    https://arxiv.org/abs/2102.02808

22. MIRNet — Learning Enriched Features for Real Image Restoration and Enhancement  
    https://arxiv.org/abs/2003.06792

23. CycleISP — CycleISP: Real Image Restoration via Improved Data Synthesis  
    https://arxiv.org/abs/2003.07761

24. DMPHN — Deep Multi-patch Hierarchical Network for Nonuniform Blur Removal  
    https://arxiv.org/abs/1909.10782

25. Efficient Posterior Sampling for Diverse Super-Resolution with Hierarchical VAE Prior  
    https://arxiv.org/abs/2205.10347

---

## ⭐ Recommended first tests

### Test A — Original project papers

Use:

- ESRGAN
- Real-ESRGAN
- SwinIR

Expected behavior: multiple candidate gaps, especially around artifacts, unseen degradations and dataset dependence.

### Test B — Classic SR progression

Use:

- VDSR
- EDSR
- RCAN

### Test C — Real-world restoration

Use:

- BSRGAN
- Real-ESRGAN
- Restormer

### Test D — Video restoration

Use:

- EDVR
- SOF-VSR
- BasicVSR

---

## 🧠 Methodology

The current prototype uses a lightweight evidence-based approach rather than an LLM-generated answer.

### 1. Paper retrieval

The app receives public arXiv URLs and retrieves the corresponding arXiv HTML paper.

### 2. Text extraction

HTML text is extracted and cleaned.

### 3. Evidence detection

Predefined keyword/phrase groups are used to identify evidence related to:

```text
artifacts
generalization
dataset dependence
```

### 4. Cross-paper comparison

A candidate gap is reported when at least two analyzed papers contain supporting evidence for the corresponding category.

### 5. Confidence

Current confidence labels are rule-based:

- **High** — artifact/generalization categories
- **Medium** — dataset/benchmark category

These labels describe the strength of the detected signal in this prototype; they are **not statistical confidence intervals**.

---

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Public arXiv URLs
  │
  ▼
arXiv HTML retrieval
  │
  ▼
Text extraction + cleaning
  │
  ▼
Evidence keyword detection
  │
  ▼
Cross-paper comparison
  │
  ▼
Candidate research gaps
  │
  ├── Supporting papers
  ├── Evidence excerpts
  ├── Confidence
  └── Potential direction
```

---

## 📁 Project structure

```text
AI-Research-Gap-Finder/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 💻 Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

## ☁️ Deployment

The project is designed for **Streamlit Community Cloud**.

Deployment:

1. Push `app.py`, `requirements.txt` and `README.md` to GitHub.
2. Open Streamlit Community Cloud.
3. Connect the GitHub repository.
4. Select `app.py` as the entrypoint.
5. Deploy.

After deployment, future code changes can be pushed to GitHub and Streamlit Community Cloud will update the deployed application.

---

## 🔐 API keys

This version does **not require Gemini, OpenAI, Hugging Face API keys, or any paid API**.

The application retrieves publicly accessible arXiv paper HTML pages directly.

---

## ⚠️ Limitations

This is an intentionally lightweight portfolio/research prototype.

### Current limitations

- Domain-specific evidence categories
- Keyword/phrase-based evidence detection
- Requires publicly accessible arXiv HTML
- Does not perform semantic novelty verification
- Does not prove that a research gap is genuinely novel
- Does not replace systematic literature review
- Candidate gaps depend on the selected papers
- A paper may contain relevant evidence that does not match the current phrase rules
- Papers without accessible HTML may not load

### Why these limitations are intentional

The project is designed to demonstrate an explainable research-assistance workflow rather than claim autonomous scientific discovery.

The system shows **why** it suggested a candidate gap by displaying supporting papers and evidence excerpts.

---

## 🔭 Possible future improvements

Potential extensions include:

- Semantic embeddings instead of only keyword matching
- LLM-assisted evidence interpretation
- Automatic paper clustering
- Citation-network analysis
- Better contradiction detection
- Section-aware evidence extraction
- Automatic limitation/future-work extraction
- More domains beyond computer vision
- Novelty checking against a larger literature corpus
- Downloadable research-gap reports
- Paper comparison visualizations

---

## 📜 Disclaimer

This project is intended for educational, research-assistance and portfolio demonstration purposes.

**Candidate research gaps are not proof of research novelty.**

Researchers should verify all suggested gaps against the current literature before using them in academic work.

---

## 👤 Project

**AI Research Gap Finder**

Built as a research-oriented AI/ML portfolio project demonstrating:

- research paper processing
- NLP-style evidence extraction
- cross-paper comparison
- explainable candidate-gap generation
- Streamlit deployment
