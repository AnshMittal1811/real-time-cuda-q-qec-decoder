# Mathematical Notation (Bra-Ket)

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
where $|\\alpha|^2 + |\\beta|^2 = 1$.
