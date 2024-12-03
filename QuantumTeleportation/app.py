from flask import Flask, request, jsonify, render_template
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram

app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/teleport', methods=['POST'])
def Teleport():
    # Get the input from the form (JSON body)
    data = request.json
    theta, phi = data.get("theta"), data.get("phi")

    # Create a quantum circuit for the state preparation
    qc = QuantumCircuit(1)
    qc.ry(theta, 0)  # Apply ry gate to qubit 0 with angle theta
    qc.rz(phi, 0)    # Apply rz gate to qubit 0 with angle phi

    # Get the state vector after applying the gates
    initial_state = Statevector.from_instruction(qc)

    # Create the quantum circuit for teleportation
    qr = QuantumRegister(3)  # 3 qubits: Alice (1), Bob (2), and the entangled pair (2 qubits)
    cr = ClassicalRegister(2)  # 2 classical bits for measurement outcomes
    circuit = QuantumCircuit(qr, cr)

    # Set up teleportation protocol
    # Qubit 0 is Alice's state
    circuit.initialize(initial_state.data, [qr[0]])  # Initialize qubit 0 with the state |ψ⟩

    # Entanglement between Alice and Bob
    circuit.h(qr[1])  # Apply Hadamard gate on Alice's qubit (qubit 1)
    circuit.cx(qr[1], qr[2])  # CNOT gate between Alice's qubit and Bob's qubit

    # Alice performs Bell-state measurement
    circuit.cx(qr[0], qr[1])  # CNOT gate on Alice's qubit 0 and qubit 1
    circuit.h(qr[0])  # Hadamard gate on Alice's qubit 0
    circuit.measure([qr[0], qr[1]], [cr[0], cr[1]])  # Measure qubits 0 and 1

    # Conditional operations based on Alice's measurement results
    circuit.z(qr[2]).c_if(cr, 1)  # If cr[0] == 1, apply Z gate to Bob's qubit (qubit 2)
    circuit.x(qr[2]).c_if(cr, 2)  # If cr[1] == 1, apply X gate to Bob's qubit (qubit 2)

    # Run the quantum circuit using the simulator
    simulator = AerSimulator()
    result = simulator.run(circuit).result()
    counts = result.get_counts()

    # Get the final quantum state of Bob's qubit after teleportation
    final_state = Statevector(result.get_statevector(circuit))

    # Return the result as a JSON response
    return jsonify({
        "final_state": final_state.data.tolist(),
        "counts": counts  # Include counts for the measurement outcomes
    })

if __name__ == "__main__":
    app.run(debug=True)
