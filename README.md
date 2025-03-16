Quantum Authentication System

Overview:
The Quantum Authentication System is a cutting-edge security platform that leverages quantum computing principles for user authentication. 
This system utilizes Quantum Fourier Transform (QFT), quantum entanglement, and classical cryptographic hashing to generate a unique, secure password authentication mechanism.

Features:
- Quantum-enhanced password hashing using Qiskit
- Secure user authentication with Flask and SQLAlchemy
- Interactive UI powered by Streamlit
- Light-themed modern UI with custom CSS styling
- User registration and authentication with a quantum-generated password signature

Technologies Used:
- Python for backend logic
- Streamlit for frontend UI
- Flask for server-side logic
- SQLAlchemy for database management
- Qiskit for quantum computing operations
- SQLite for storing user credentials

How It Works: 
1. User Registration:
  Users enter a username and password. The system quantum-hashes the password using Quantum Fourier Transform (QFT) and SHA-256 pre-processing. The hashed password is stored in the SQLite database.

2. User Authentication:
  Users enter their credentials. The system recomputes the quantum hash of the entered password. If the computed hash matches the stored hash, authentication is successful.

3. Quantum Circuit Operations:
  The password is pre-processed using SHA-256. The first 5 hex characters (20 bits) are converted to quantum states. A Quantum Fourier Transform (QFT) is applied. Entanglement gates (CNOT) are used to link qubits. The inverse QFT is applied. The system measures the quantum state to generate a deterministic quantum signature.

Security Considerations:
1. Quantum Resilience: Uses quantum computations alongside classical hashing for enhanced security.
2. SHA-256 Pre-processing: Ensures deterministic inputs for quantum circuits.
3. Quantum Hashing: Uses QFT-based signatures, making it infeasible for traditional attacks.
4. Database Security: Passwords are not stored in plaintext; instead, only quantum-hashed values are stored.

Future Enhancements:
1. Implementing real quantum hardware execution instead of a simulator.
2. Enhancing multi-factor authentication using quantum key distribution (QKD).
3. Introducing biometric authentication as an additional security layer.
