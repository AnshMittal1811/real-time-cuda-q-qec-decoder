import os

files = {
    "mkdocs.yml": """site_name: Real-Time CUDA-Q QEC Decoder
site_url: https://AnshMittal1811.github.io/real-time-cuda-q-qec-decoder/
repo_url: https://github.com/AnshMittal1811/real-time-cuda-q-qec-decoder
repo_name: AnshMittal1811/real-time-cuda-q-qec-decoder
edit_uri: edit/main/docs/
theme:
  name: material
  features:
    - navigation.sections
    - navigation.footer
    - toc.integrate
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: deep purple
      accent: deep purple
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: deep purple
      accent: deep purple
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - admonition
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - tables
  - toc:
      permalink: true
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - javascripts/mathjax.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Home: index.md
  - Architecture: architecture.md
  - Timeline: timeline.md
  - Quantum Computing:
    - Qubits (Creation & Types): quantum_computing/qubits.md
    - The Bloch Sphere: quantum_computing/bloch_sphere.md
    - Bra-Ket Notation: quantum_computing/bra_ket.md
    - Quantum Mechanics: quantum_computing/quantum_mechanics.md
    - Quantum Tunnelling: quantum_computing/quantum_tunnelling.md
    - Quantum Error Correction: quantum_computing/qec.md
    - Quantum Libraries: quantum_computing/libraries.md
  - Quantum Generative AI Hub: qml/generative_quantum_ai.md
  - Project Connection: project_connection.md""",
    "docs/javascripts/mathjax.js": """window.MathJax = {
  tex: {
    inlineMath: [["\\\\(", "\\\\)"]],
    displayMath: [["\\\\[", "\\\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};""",
    "docs/qml/generative_quantum_ai.md": """# Unified Quantum Generative AI Research Hub

This page consolidates cutting-edge research into Quantum Generative AI, bridging the gap between real-time Quantum Error Correction (QEC) and generative modeling techniques like Diffusion, NeRFs, and LLMs.

---

## 1. Quantum Diffusion Models (QDM)
*Based on: arXiv:2311.15444v1*

Quantum Diffusion Models replace classical Artificial Neural Networks (ANNs) with **Parameterized Quantum Circuits (PQCs)** to perform the denoising process directly on quantum states.

- **Core Mechanism:** A forward Markov chain adds noise classically, while a PQC is trained to approximate the reverse (denoising) trajectory.
- **Key Advantage:** Direct manipulation of quantum state amplitudes $|x_t\\rangle \rightarrow |x_{t-1}\\rangle$ allows for generating distributions with features that scale exponentially with the number of qubits.
- **Performance:** Successfully demonstrated on MNIST, achieving high-quality sample generation on NISQ devices with fewer parameters than classical counterparts.

## 2. Quantum Radiance Fields (QRF)
*Based on: arXiv:2211.03418*

Applying Quantum Computing to the challenge of photorealistic rendering.

- **Innovation:** QRF utilizes quantum circuits and quantum volume rendering to represent 3D scenes implicitly.
- **Quantum Speedup:** Exploits quantum parallelism to handle the intensive numerical integration required for ray tracing.
- **Non-linearity:** Leverages higher-order quantum non-linearity to capture high-frequency scene details that traditional NeRFs often struggle with.

## 3. Quantum Gaussian Splatting (QGS)
*Based on: QuantumGS Repository*

Integrating quantum-enhanced optimization with 3D Gaussian Splatting.

- **Approach:** Utilizing quantum search or variational algorithms to optimize the parameters (position, covariance, opacity) of 3D Gaussians.
- **Impact:** Potentially reduces the time-to-convergence for complex scene reconstructions by leveraging quantum-classical hybrid optimization loops.

## 4. Quantum Variational Autoencoders (QVAE)
*Based on: arXiv:1802.05779*

Generative modeling where the latent space is governed by quantum dynamics.

- **Mechanism:** Implements the latent generative process using a **Quantum Boltzmann Machine (QBM)**.
- **Sampling:** Uses quantum computers as effective sampling devices within the latent space, maximizing a "quantum" lower bound to the log-likelihood.

## 5. Quantum Large Language Models (QLLM)
*Based on: arXiv:2602.05047v1*

Scaling quantum attention mechanisms for natural language processing.

- **Concept:** Replacing classical attention matrices with quantum kernels to capture long-range dependencies in text using Hilbert space embeddings.
- **Future Integration:** Bridging the transformer decoder used in our **Real-Time QEC Decoder** with quantum-native transformer blocks.

---

## Technical Integration with Real-Time QEC
The research into Quantum Generative AI is directly relevant to the `real-time-cuda-q-qec-decoder` project in several ways:

1. **Synthetic Syndrome Generation:** Quantum Diffusion and QVAEs can be used to generate high-fidelity, synthetic QEC syndrome data to train more robust neural decoders.
2. **Hybrid Inference:** Our project's use of PyTorch Transformer Decoders serves as a bridge; as QLLMs mature, the classical blocks can be swapped for quantum-native kernels.
3. **GPU-Quantum Synergy:** Much like QRF and QGS rely on NVIDIA GPU acceleration for rasterization, our decoder utilizes **CUDA-Q** to align real-time decoding with quantum state preparation.

### Mathematical Framework
Quantum states are represented in Dirac notation:
\\\\[ |\\\\psi\\\\rangle = \\\\alpha|0\\\\rangle + \\\\beta|1\\\\rangle \\\\]

The infidelity loss used in training our PQC models is defined as:
\\\\[ L(\\\\theta) = 1 - E[F(\\\\hat{P}(\\\\theta, t)|x_{t+1}\\\\rangle, |x_t\\\\rangle)] \\\\]
where $F$ is the quantum fidelity.
""",
    "docs/quantum_computing/qubits.md": """# Qubits: The Building Blocks of Quantum Computing

## What is a Qubit?
A qubit, or quantum bit, is the fundamental unit of quantum information. Unlike classical bits that can only be 0 or 1, a qubit can exist in a **superposition** of both states simultaneously. It is only upon measurement that the qubit collapses into a definite 0 or 1.

## How are Qubits Created?
Creating a qubit requires isolating a quantum system so it can maintain its delicate quantum state without decohering due to environmental noise. 

## Different Types of Qubits
There are several leading physical implementations for qubits:

1. **Superconducting Qubits (Transmons):**
   - **How it works:** Uses superconducting circuits (often Niobium or Aluminum) cooled to near absolute zero. Josephson junctions create non-linear LC oscillators.
   - **Pioneers:** Google (Sycamore), IBM (Eagle, Condor, Heron).
2. **Trapped Ions:**
   - **How it works:** Individual ions are trapped in a vacuum using electromagnetic fields and manipulated with lasers.
   - **Pioneers:** IonQ, Quantinuum.
3. **Topological Qubits:**
   - **How it works:** Uses anyons (like Majorana fermions) whose quantum states are braided topologically, making them inherently resistant to local noise.
   - **Pioneers:** Microsoft.
4. **Photonic Qubits:**
   - **How it works:** Encodes information in the properties of light (e.g., polarization or phase of photons).
   - **Pioneers:** PsiQuantum, Xanadu.
5. **Neutral Atoms:**
   - **How it works:** Uses optical tweezers to hold highly excited Rydberg atoms in place.
   - **Pioneers:** QuEra Computing.""",
    "docs/quantum_computing/bloch_sphere.md": """# The Bloch Sphere

The **Bloch sphere** is a geometrical representation of the pure state space of a two-level quantum mechanical system (a qubit).

## Visualizing Quantum States
- The North Pole represents the classical state \\\\(|0\\\\rangle\\\\).
- The South Pole represents the classical state \\\\(|1\\\\rangle\\\\).
- The surface of the sphere represents all possible pure states (superpositions) of the qubit.

\\\\[ |\\\\psi\\\\rangle = \\\\cos(\\\\theta/2)|0\\\\rangle + e^{i\\\\phi}\\\\sin(\\\\theta/2)|1\\\\rangle \\\\]

When quantum operations (gates) are applied to a qubit, they can be visualized as rotations around the axes (X, Y, Z) of the Bloch sphere.""",
    "docs/quantum_computing/bra_ket.md": """# Mathematical Notation (Bra-Ket)

**Dirac notation**, or **Bra-Ket notation**, is the standard mathematical language for quantum mechanics.

- **Ket $|\\\\psi\\\\rangle$**: Represents a column vector, denoting a quantum state.
- **Bra $\\\\langle\\\\psi|$**: Represents a row vector (the complex conjugate transpose of the Ket).
- **Inner Product (Bra-Ket) $\\\\langle\\\\phi|\\\\psi\\\\rangle$**: The dot product of two states, representing the probability amplitude of state $\\\\psi$ collapsing into state $\\\\phi$.

### Standard Basis
The computational basis states are defined as:
- $|0\\\\rangle = \\\\begin{bmatrix} 1 \\\\\\\\ 0 \\\\end{bmatrix}$
- $|1\\\\rangle = \\\\begin{bmatrix} 0 \\\\\\\\ 1 \\\\end{bmatrix}$

### Superposition
A general qubit state is written as a linear combination of basis states:
$|\\\\psi\\\\rangle = \\\\alpha|0\\\\rangle + \\\\beta|1\\\\rangle$
where $|\\\\alpha|^2 + |\\\\beta|^2 = 1$.""",
    "docs/quantum_computing/quantum_mechanics.md": """# Quantum Mechanics Principles

Understanding quantum computing requires grasping three core phenomena of quantum mechanics:

1. **Superposition:** The ability of a quantum system to be in multiple states simultaneously. A qubit is not strictly 0 or 1, but a weighted combination of both until observed.
2. **Entanglement:** A uniquely quantum phenomenon where two or more particles become correlated such that the state of one instantly influences the state of the other, regardless of distance. Albert Einstein famously called this "spooky action at a distance."
3. **Interference:** Quantum algorithms use the wave-like nature of probability amplitudes. Just like ripples in a pond, quantum states can interfere constructively (amplifying correct answers) or destructively (canceling out wrong answers).""",
    "docs/quantum_computing/quantum_tunnelling.md": """# Quantum Tunnelling

**Quantum tunnelling** is the quantum mechanical phenomenon where a subatomic particle passes through a potential barrier that it could not surmount according to classical mechanics.

### Role in Quantum Computing
Quantum tunnelling is the fundamental mechanism behind **Quantum Annealing** (used by companies like D-Wave). 

In quantum annealing, the system is initialized in a superposition of all possible solutions (a flat energy landscape). As the system evolves, barriers arise. If the barriers are thin enough, the system can "tunnel" through them to find the absolute lowest energy point (the optimal solution), completely bypassing local minimums that would trap classical optimization algorithms.""",
    "docs/quantum_computing/qec.md": """# Quantum Error Correction

Quantum information is highly susceptible to **decoherence** caused by environmental noise (heat, electromagnetic radiation, etc.). **Quantum Error Correction (QEC)** is the field of computer science and physics dedicated to mitigating these errors.

## Surface Codes
Because we cannot directly measure a data qubit without destroying its superposition, we encode a single "logical" qubit into a 2D grid of noisy "physical" qubits. 
By performing periodic **parity measurements** (stabilizers) on adjacent qubits, we can detect if an error (bit-flip or phase-flip) has occurred without collapsing the data.

## The Role of the Decoder
The stream of parity measurements forms a **syndrome**. 
A **Decoder** (like the `real-time-cuda-q-qec-decoder`) takes this syndrome data and solves a matching problem in real-time to infer which physical errors occurred, allowing the control system to apply software-level corrections and keep the logical qubit stable.""",
    "docs/quantum_computing/libraries.md": """# Libraries and Frameworks

The quantum software ecosystem is rich and diverse, bridging classical computing and quantum hardware:

- **NVIDIA CUDA-Q:** A comprehensive, open-source C++ and Python platform for building quantum-classical applications. It seamlessly integrates GPU acceleration with quantum circuit simulation.
- **Qiskit (IBM):** An open-source SDK for working with quantum computers at the level of pulses, circuits, and application modules.
- **Cirq (Google):** A Python software library for writing, manipulating, and optimizing quantum circuits, designed for NISQ hardware.
- **PennyLane (Xanadu):** A cross-platform Python library for differentiable programming of quantum computers, heavily used in Quantum Machine Learning.""",
    "docs/qml/introduction.md": """# Introduction to Quantum Machine Learning (QML)

**Quantum Machine Learning (QML)** is the intersection of quantum physics and machine learning. It investigates how quantum computers can accelerate, improve, or alter classical machine learning algorithms, and conversely, how classical ML can improve quantum technologies.

### Key Concepts
- **Quantum Neural Networks (QNNs):** Parameterized quantum circuits where the rotation angles are trained using classical gradient descent to minimize a loss function.
- **Variational Quantum Eigensolver (VQE):** A hybrid algorithm that uses a quantum computer to prepare a trial state and measure its energy, while a classical optimizer updates the parameters.
- **Feature Maps:** Encoding classical data (like images or text) into a high-dimensional quantum Hilbert space to identify complex non-linear patterns.""",
    "docs/qml/timeline.md": """# Convergence Timeline

The path to modern Quantum AI is a convergence of three parallel tracks: Machine Learning software, GPU Hardware acceleration, and Quantum Physics breakthroughs.

```mermaid
timeline
    title Convergence of ML, GPUs, and Quantum Physics
    section Machine Learning
        2012 : Deep Learning Boom (AlexNet)
        2017 : Transformers Introduced (Attention is All You Need)
        2020 : Large Language Models (GPT-3)
        2024 : Agentic AI & RLHF Dominance
    section GPU Hardware
        2012 : NVIDIA Kepler (K20)
        2017 : NVIDIA Volta (V100) Tensor Cores
        2022 : NVIDIA Hopper (H100) TMA and Transformer Engine
        2024 : NVIDIA Blackwell (B200) FP4 / FP6 Precision
    section Quantum Physics & Hardware
        2019 : Google Sycamore (Quantum Supremacy Demonstration)
        2021 : IBM Eagle (127-Qubit Processor)
        2024 : Microsoft Topological Qubit Breakthroughs
        2025 : Google TurboQuant & Expansions in Quantum AI
```""",
    "docs/project_connection.md": """# Tying It All Together: Research & Real-Time QEC

How does the `real-time-cuda-q-qec-decoder` fit into the broader landscape of Machine Learning, GPUs, and Quantum Computing?

### The Interdisciplinary Challenge
Quantum computers generate massive amounts of noisy parity data (syndromes). If we cannot decode this data and correct errors in **real-time**, the quantum computer will fail to execute long algorithms (like Shor's or Grover's).

1. **From Quantum Physics:** The syndrome data originates from surface codes running on physical qubits (e.g., transmon or topological qubits).
2. **From Machine Learning:** The decoder utilizes a PyTorch-trained **Transformer Decoder**—a direct descendant of modern LLM architectures—adapted for spatial and temporal syndrome patterns instead of text.
3. **From GPU Hardware:** Real-time decoding constraints (microseconds) mandate avoiding host-to-device bottlenecks. We utilize NVIDIA **TMA (Tensor Memory Accelerator)**, **mbarrier synchronizations**, and **TensorRT** INT4/FP8 optimizations.

### Why This Research Matters
By merging these three domains, this project demonstrates that **machine learning models can operate within the strict real-time control loops of quantum hardware**. The implementation of RLHF to fine-tune the decoder dynamically against drifting physical noise models highlights how AI will be an indispensable component of building fault-tolerant quantum systems in the late 2020s.""",
    ".github/workflows/gh-pages.yml": """name: Deploy MkDocs to GitHub Pages
on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.x
      - run: echo "cache_id=$(( $(date --utc +%V) ))" >> $GITHUB_ENV
      - uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ env.cache_id }}
          path: .cache
          restore-keys: |
            mkdocs-material-
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

print("Documentation site generated successfully.")
