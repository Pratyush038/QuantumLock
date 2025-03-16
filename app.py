import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import QFT
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib
from dotenv import load_dotenv
from models import db, User
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quantum_auth.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(flask_app)

# Create database tables
with flask_app.app_context():
    db.create_all()

# Configure Streamlit page
st.set_page_config(
    page_title="Quantum Authentication System",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for light theme UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(90deg, #2b5876 0%, #4e4376 100%);
        border: none;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(0, 0, 0, 0.2);
        color: #333333;
    }
    .quantum-circuit {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3, h4 {
        color: #2b5876 !important;
    }
    p, li {
        color: #333333 !important;
    }
    .expander {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'circuit_image' not in st.session_state:
    st.session_state.circuit_image = None

def quantum_hash(password: str, seed=None) -> str:
    """
    Create a deterministic quantum hash using Qiskit quantum circuits
    
    Parameters:
    password (str): Password to hash
    seed (int): Optional seed for deterministic results
    
    Returns:
    str: Hexadecimal hash value
    """
    # Set random seed if provided
    if seed is not None:
        np.random.seed(seed)
    
    # Pre-process the password with SHA-256 to get a consistent length and bit pattern
    # This ensures a more stable input for the quantum circuit
    sha_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    binary = ''.join(format(int(c, 16), '04b') for c in sha_hash[:5])  # Use first 5 hex chars (20 bits)
    
    # Create quantum registers
    n_qubits = len(binary)  # Using 20 qubits from SHA-256 pre-processing
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Apply quantum operations
    # Initialize qubits based on password bits
    for i, bit in enumerate(binary):
        if bit == '1':
            qc.x(qr[i])
    
    # Apply Hadamard gates to create superposition
    qc.h(qr)
    
    # Apply QFT
    qc.append(QFT(n_qubits), range(n_qubits))
    
    # Add entanglement
    for i in range(n_qubits-1):
        qc.cx(qr[i], qr[i+1])
    
    # Inverse QFT
    qc.append(QFT(n_qubits).inverse(), range(n_qubits))
    
    # Measure qubits
    qc.measure(qr, cr)
    
    # Execute the circuit with shots=1024 to get the most probable outcome
    backend = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, backend)
    job = backend.run(transpiled_circuit, shots=1024, seed_simulator=42 if seed is None else seed)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Get the most frequent measurement outcome
    measured_state = max(counts.items(), key=lambda x: x[1])[0]
    
    # Convert binary to hexadecimal for shorter hash
    hash_value = hex(int(measured_state, 2))[2:]
    
    # Return combined hash (add SHA-256 suffix for extra security)
    final_hash = hash_value + sha_hash[-16:]
    
    return final_hash

def main():
    # Display title with custom styling
    st.markdown(
        "<h1 style='text-align: center; color: #2b5876; margin-bottom: 2em;'>"
        "Quantum Authentication System</h1>",
        unsafe_allow_html=True
    )
    with st.expander("⚠️ Performance Warning"):
        st.markdown("""
        This application uses multiple quantum computing libraries, including Qiskit and Qiskit Aer, which may require significant computational resources. 
        Performance may vary depending on your system's CPU, available RAM, and whether your processor supports multi-threading. 
        Running on lower-end machines may result in slower execution times, especially during quantum circuit simulations. 
        For optimal performance, consider running this on a system with a high-performance CPU or enabling GPU acceleration where possible. """)
    with st.expander("How Quantum Authentication Works"):
        st.markdown("""
        This system uses quantum computing principles for secure authentication:
        
        1. **Quantum Superposition**: Your password is encoded into quantum states
        2. **Quantum Fourier Transform**: Applies quantum transformations
        3. **Quantum Entanglement**: Creates unique quantum signatures
        4. **Measurement**: Collapses quantum states into classical bits
        
        The quantum circuit includes:
        - Hadamard gates for superposition
        - Quantum Fourier Transform
        - Controlled-NOT gates for entanglement
        - Quantum measurements
        
        For consistent results, we use:
        - A fixed seed for simulation
        - Pre-processing with SHA-256
        - Multiple shots to find the most probable outcome
        """)
    
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                submit_login = st.form_submit_button("Login")
                
                if submit_login:
                    if username and password:
                        # Use fixed seed=42 for consistent hashing
                        hashed_password = quantum_hash(password, seed=42)
                        with flask_app.app_context():
                            user = User.query.filter_by(username=username).first()
                            if user and user.password_hash == hashed_password:
                                user.last_login = datetime.utcnow()
                                db.session.commit()
                                st.session_state.authenticated = True
                                st.session_state.username = username
                                st.success("Quantum authentication successful! 🌟")
                                st.rerun()
                            else:
                                st.error("Invalid quantum signature")
                    else:
                        st.error("Please fill in all fields")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Username", key="register_username")
                new_password = st.text_input("Password", type="password", key="register_password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_register = st.form_submit_button("Register")
                
                if submit_register:
                    if new_username and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Quantum states do not match")
                        elif len(new_password) < 8:
                            st.error("Quantum signature requires at least 8 characters")
                        else:
                            with flask_app.app_context():
                                if User.query.filter_by(username=new_username).first():
                                    st.error("Quantum state already exists")
                                else:
                                    # Use fixed seed=42 for consistent hashing
                                    hashed_password = quantum_hash(new_password, seed=42)
                                    new_user = User(
                                        username=new_username,
                                        password_hash=hashed_password
                                    )
                                    db.session.add(new_user)
                                    db.session.commit()
                                    st.success("Quantum state registered successfully! 🌟")
                    else:
                        st.error("Please fill in all fields")
    
    else:
        st.markdown(
            f"<h2 style='text-align: center; color: #2b5876;'>Welcome to the Quantum Realm, {st.session_state.username}! ⚛️</h2>",
            unsafe_allow_html=True
        )
        
        # Display quantum metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Quantum State", "Coherent", delta="stable")
        with col2:
            st.metric("Entanglement", "99.9%", delta="0.1%")
        
        # Display registered quantum states
        with flask_app.app_context():
            users = User.query.all()
            st.markdown("### Quantum State Registry")
            for user in users:
                last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "Never"
                st.markdown(f"- 🌌 {user.username} (Last quantum interaction: {last_login})")
        
        if st.button("Collapse Quantum State (Logout)"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

if __name__ == "__main__":
    main()
