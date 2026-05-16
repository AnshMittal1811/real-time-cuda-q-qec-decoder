import os

files = {
    "mkdocs.yml": """site_name: Real-Time CUDA-Q QEC Decoder
site_url: https://AnshMittal1811.github.io/real-time-cuda-q-qec-decoder/
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
  - Quantum Machine Learning:
    - Introduction to QML: qml/introduction.md
    - Convergence Timeline: qml/timeline.md
    - Quantum AI: qml/quantum_ai.md
  - Project Connection: project_connection.md""",
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
- The North Pole represents the classical state $|0\\rangle$.
- The South Pole represents the classical state $|1\\rangle$.
- The surface of the sphere represents all possible pure states (superpositions) of the qubit.

```math
|\\psi\\rangle = \\cos(\\theta/2)|0\\rangle + e^{i\\phi}\\sin(\\theta/2)|1\\rangle
```

When quantum operations (gates) are applied to a qubit, they can be visualized as rotations around the axes (X, Y, Z) of the Bloch sphere.""",
    "docs/quantum_computing/bra_ket.md": """# Mathematical Notation (Bra-Ket)

**Dirac notation**, or **Bra-Ket notation**, is the standard mathematical language for quantum mechanics.

- **Ket $|\\psi\\rangle$**: Represents a column vector, denoting a quantum state.
- **Bra $\\langle\\psi|$**: Represents a row vector (the complex conjugate transpose of the Ket).
- **Inner Product (Bra-Ket) $\\langle\\phi|\\psi\\rangle$**: The dot product of two states, representing the probability amplitude of state $\\psi$ collapsing into state $\\phi$.

### Standard Basis
The computational basis states are defined as:
- $|0\\rangle = \\begin{bmatrix} 1 \\\\ 0 \\end{bmatrix}$
- $|1\\rangle = \\begin{bmatrix} 0 \\\\ 1 \\end{bmatrix}$

### Superposition
A general qubit state is written as a linear combination of basis states:
$|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle$
where $|\\alpha|^2 + |\\beta|^2 = 1$.""",
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
    "docs/qml/quantum_ai.md": """# Quantum AI and its Subtopics

As quantum hardware matures, Quantum AI explores replacing classical neural network architectures with quantum equivalents.

### Subtopics
1. **Quantum Generative Adversarial Networks (QGANs):** Using quantum circuits as the generator to produce quantum data (or classical data encoded in quantum states), while a classical or quantum discriminator tries to distinguish them from real data.
2. **Quantum Convolutional Neural Networks (QCNNs):** Adapting the concept of local receptive fields and pooling layers to quantum circuits to analyze quantum states or encoded images, highly useful for quantum phase recognition.
3. **Quantum Reinforcement Learning (QRL):** A quantum agent interacts with a classical or quantum environment. Quantum superposition allows the agent to explore multiple actions simultaneously, theoretically speeding up the learning of optimal policies.
4. **Google TurboQuant:** Google advancements in highly optimized, massive-scale quantum chemistry and physics simulations, bridging classical AI with quantum state representations to discover new materials and drugs.""",
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
