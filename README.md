# Grover on Quantum Cryptanalysis

This work is part of CS614: Quantum Symmetric-Key Cryptanalysis offered by [Dr. Dhiman Saha](http://dhimans.in/) at IIT Bhilai.

Grover's search algorithm promises to recover a block cipher's key in $O(\sqrt{N})$ calls to quantum oracle where $N$ is the key search space. To apply Grover's search on a block cipher, one needs to implement it in a quantum circuit. This paper studies implementation of quantum circuits of hardware as well as software efficient block ciphers and Grover's attack on them. Specifically, we study SAES, SIMON 2n/mn, PRESENT, and AES-128 and optimize the count of qubits. Based on the submission requirements of NIST, we investigate the cost of quantum key search attacks with a depth constraint and offer ways for reducing oracle depth while requiring more qubits for AES-128.

We provide python implementation of Grover's Oracle for SAES as part of this work and quantum resource estimates. We test on IBMQ simulators and verify the results.

For more details, see the [report](https://github.com/Gopal-Dahale/QSKC-Grover/blob/main/quantum_grover_applications.pdf) and/or [presentation](https://github.com/Gopal-Dahale/QSKC-Grover/blob/main/quantum_grover_applications_presentation.pdf). Below we have described the directory structure.

## [AES](https://github.com/Gopal-Dahale/QSKC-Grover/tree/main/AES)

We implemented AES using python for testing purpose. The directory also contains comparsion of depths of Toffoli gate and AND gate. The AND gate was used in the construction of Quantum AES in the paper [Implementing Grover oracles for quantum key search on AES and LowMC](https://eprint.iacr.org/2019/1146.pdf).

## [QC_hash_claw](https://github.com/Gopal-Dahale/QSKC-Grover/tree/main/QC_hash_claw)

Implementation of BHT algorithm for finding hash collisions and implementation of algorithm for finding claws in functions which are used in various cryptographic protocols. This work was adapted from the [Quantum Cryptanalysis of Hash and Claw-Free Functions](https://dl.acm.org/doi/pdf/10.1145/261342.261346).

## [SAES](https://github.com/Gopal-Dahale/QSKC-Grover/tree/main/SAES)

We implemented classical version of SAES in python. We implemented the Quantum SAES as studied in [Quantum Grover Attack on the Simplified-AES](https://dl.acm.org/doi/10.1145/3185089.3185122#sec-ref) and call it SAES18 (as it was published in 2018) . They used 64 qubits with 8 ancilla qubits. We were unable to test it due to computational and time constraints. Complete implementation of encryption oracle of SAES18 in python using Qiskit and partially complete implementation using libquantum in C is provided.

[Grover on Simplified AES](https://ieeexplore.ieee.org/abstract/document/9642017) uses on 32 qubits (16 for key expansion and 16 for rounds) in their work. We call it SAES21 (as it was published in 2021). Implementation of SAES21 and Grover's Oracles in python is provided. libquantum implementation in C is also provided for the encryption part.

## [present](https://github.com/Gopal-Dahale/QSKC-Grover/tree/main/present)

We impelemented the PRESENT Sbox as described in [Efficient Implementation of PRESENT and GIFT on Quantum Computers](https://www.mdpi.com/2076-3417/11/11/4776). They use [LIGHTER-R tool](https://ieeexplore.ieee.org/document/9088027) which provides optimized reversible circuit implementation for Sboxes. The SBox described in the paper has a depth of 11 and uses 5 CNOT, 4 CCNOT, 2 X and 2 SWAP gates. This is much less than the naive implemenation of Sbox using its algebraic normal form.

## [source-codes](https://github.com/Gopal-Dahale/QSKC-Grover/tree/main/source-codes)

This contains source codes of [Quantum implementation and resource estimates for Rectangle and Knot](https://link.springer.com/article/10.1007/s11128-021-03307-6), [Evaluation of Grover’s algorithm toward quantum cryptanalysis on ChaCha](https://link.springer.com/article/10.1007/s11128-021-03322-7), [Implementing Grover oracles for quantum key search on AES and LowMC](https://eprint.iacr.org/2019/1146.pdf), [Evaluation of Quantum Cryptanalysis on SPECK](https://www.researchgate.net/publication/346774631_Evaluation_of_Quantum_Cryptanalysis_on_SPECK) and [Grover on SIMON](https://link.springer.com/article/10.1007/s11128-020-02844-w).

These are not my implemenatations and are open sourced already. These are just for reference purposes.
