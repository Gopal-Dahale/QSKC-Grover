# Grover on Quantum Cryptanalysis

This work is part of CS614: Quantum Symmetric-Key Cryptanalysis offered by [Dr. Dhiman Saha](http://dhimans.in/) at IIT Bhilai.

Grover's search algorithm promises to recover a block cipher's key in $O(\sqrt{N})$ calls to quantum oracle where $N$ is the key search space. To apply Grover's search on a block cipher, one needs to implement it in a quantum circuit. This paper studies implementation of quantum circuits of hardware as well as software efficient block ciphers and Grover's attack on them. Specifically, we study SAES, SIMON 2n/mn, PRESENT, and AES-128 and optimize the count of qubits. Based on the submission requirements of NIST, we investigate the cost of quantum key search attacks with a depth constraint and offer ways for reducing oracle depth while requiring more qubits for AES-128.

We provide python implementation of Grover's Oracle for SAES as part of this work and quantum resource estimates. We test on IBMQ simulators and verify the results.

For more details, see the [report](https://github.com/Gopal-Dahale/QSKC-Grover/blob/main/quantum_grover_applications.pdf) and/or [presentation](https://github.com/Gopal-Dahale/QSKC-Grover/blob/main/quantum_grover_applications_presentation.pdf).

## AES

We implemented AES using python for testing purpose. The directory also contains comparsion of depths of Toffoli gate and AND gate. The AND gate was used in the construction of Quantum AES in the paper [Implementing Grover oracles for quantum key search on AES and LowMC](https://eprint.iacr.org/2019/1146.pdf).

## QC_hash_claw

Implementation of BHT algorithm for finding hash collisions and implementation of algorithm for finding claws in functions which are used in various cryptographic protocols. This work was adapted from the [Quantum Cryptanalysis of Hash and Claw-Free Functions](https://dl.acm.org/doi/pdf/10.1145/261342.261346).

# SAES

We implemented classical version of SAES in python.
