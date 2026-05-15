# Quantum Error Correction

Quantum information is highly susceptible to **decoherence** caused by environmental noise (heat, electromagnetic radiation, etc.). **Quantum Error Correction (QEC)** is the field of computer science and physics dedicated to mitigating these errors.

## Surface Codes
Because we cannot directly measure a data qubit without destroying its superposition, we encode a single "logical" qubit into a 2D grid of noisy "physical" qubits. 
By performing periodic **parity measurements** (stabilizers) on adjacent qubits, we can detect if an error (bit-flip or phase-flip) has occurred without collapsing the data.

## The Role of the Decoder
The stream of parity measurements forms a **syndrome**. 
A **Decoder** (like the `real-time-cuda-q-qec-decoder`) takes this syndrome data and solves a matching problem in real-time to infer which physical errors occurred, allowing the control system to apply software-level corrections and keep the logical qubit stable.
