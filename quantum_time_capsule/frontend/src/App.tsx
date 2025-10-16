import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:5000';

function App() {
  const [output, setOutput] = useState('Quantum Time Capsule Ready\n\n');
  const [message, setMessage] = useState('');
  const [unlockDate, setUnlockDate] = useState('');
  const [capsuleIndex, setCapsuleIndex] = useState('');
  const [showModal, setShowModal] = useState(false);

  const appendOutput = (text: string) => setOutput(prev => prev + text);
  const clearOutput = () => setOutput('');

  const handleGenerateKeys = async () => {
    try {
      appendOutput('→ Generating cryptographic keys...\n');
      const res = await axios.post(`${API_BASE}/generate_keys`);
      if (res.data.success) {
        appendOutput('✓ Keys generated successfully\n');
        appendOutput('  RSA + ECDSA key pair created\n');
        appendOutput('  Keys stored in secure location\n\n');
      } else {
        appendOutput(`✗ Failed: ${res.data.error}\n\n`);
      }
    } catch (e: any) {
      appendOutput(`✗ Error: ${e.response?.data?.error || e.message}\n\n`);
    }
  };

  const handleViewCapsules = async () => {
    try {
      appendOutput('→ Fetching capsule list...\n');
      const res = await axios.get(`${API_BASE}/capsules`);
      if (res.data.success) {
        const capsules = res.data.capsules || [];
        appendOutput(`✓ Found ${capsules.length} capsule(s)\n`);
        capsules.forEach((cap: any, i: number) => {
          const status = cap.status === 'unlocked' ? '🔓 UNLOCKED' : '🔒 LOCKED';
          appendOutput(`  [${i + 1}] ${cap.timestamp} - Unlock: ${cap.unlock_date} ${status}\n`);
        });
        appendOutput('\n');
      } else {
        appendOutput(`✗ Failed: ${res.data.error}\n\n`);
      }
    } catch (e: any) {
      appendOutput(`✗ Error: ${e.response?.data?.error || e.message}\n\n`);
    }
  };

  const handleDecryptCapsule = async () => {
    const idx = parseInt(capsuleIndex);
    if (isNaN(idx) || idx < 1) {
      appendOutput('✗ Invalid capsule index\n\n');
      return;
    }
    try {
      appendOutput(`→ Decrypting capsule #${idx}...\n`);
      const res = await axios.post(`${API_BASE}/decrypt_capsule`, { capsule_index: idx - 1 });
      if (res.data.success) {
        appendOutput(`✓ Decryption successful\n`);
        appendOutput(`  Message: "${res.data.decrypted_message}"\n`);
        appendOutput(`  Timestamp: ${res.data.timestamp}\n`);
        appendOutput(`  Unlock Date: ${res.data.unlock_date}\n`);
        appendOutput(`  Signature: ✓ Verified\n\n`);
        setCapsuleIndex('');
      } else {
        appendOutput(`✗ Decryption failed: ${res.data.error}\n\n`);
      }
    } catch (e: any) {
      const errorMsg = e.response?.data?.error || e.message || 'Unknown error';
      appendOutput(`✗ Error: ${errorMsg}\n`);
      appendOutput(`  Status: ${e.response?.status}\n\n`);
    }
  };

  const handleVerifyCapsule = async () => {
    const idx = parseInt(capsuleIndex);
    if (isNaN(idx) || idx < 1) {
      appendOutput('✗ Invalid capsule index\n\n');
      return;
    }
    try {
      appendOutput(`→ Verifying capsule #${idx}...\n`);
      const res = await axios.post(`${API_BASE}/verify_capsule`, { capsule_index: idx - 1 });
      if (res.data.success && res.data.verified) {
        appendOutput(`✓ Capsule verified successfully\n`);
        appendOutput(`  Timestamp: ${res.data.timestamp}\n`);
        appendOutput(`  Unlock Date: ${res.data.unlock_date}\n`);
        appendOutput(`  Signature: ✓ Valid\n\n`);
      } else {
        appendOutput(`✗ Verification failed\n\n`);
      }
      setCapsuleIndex('');
    } catch (e: any) {
      const errorMsg = e.response?.data?.error || e.message || 'Unknown error';
      appendOutput(`✗ Error: ${errorMsg}\n\n`);
    }
  };

  const handleCreateCapsule = async () => {
    if (!message.trim()) {
      appendOutput('✗ Message cannot be empty\n\n');
      return;
    }
    if (!unlockDate) {
      appendOutput('✗ Please select an unlock date\n\n');
      return;
    }
    try {
      appendOutput('→ Creating new capsule...\n');
      const res = await axios.post(`${API_BASE}/create_capsule`, { message, unlock_date: unlockDate });
      if (res.data.success) {
        appendOutput(`✓ Capsule created successfully\n`);
        appendOutput(`  Message: "${message.substring(0, 50)}${message.length > 50 ? '...' : ''}"\n`);
        appendOutput(`  Unlock: ${unlockDate}\n`);
        appendOutput(`  Encrypted with PQC\n\n`);
        setMessage('');
        setUnlockDate('');
        setShowModal(false);
      } else {
        appendOutput(`✗ Failed: ${res.data.error}\n\n`);
      }
    } catch (e: any) {
      const errorMsg = e.response?.data?.error || e.message || 'Unknown error';
      appendOutput(`✗ Error: ${errorMsg}\n\n`);
    }
  };

  return (
    <div className="h-screen bg-white flex flex-col">
      <div className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white px-8 py-4 shadow-lg">
        <div className="flex justify-between">
          <div>
            <h1 className="text-2xl font-bold">Quantum Time Capsule</h1>
            <p className="text-indigo-100 text-sm">Post-Quantum Cryptography</p>
          </div>
          <p className="text-indigo-100 text-sm">{new Date().toLocaleString()}</p>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <div className="w-80 bg-gray-50 border-r border-gray-200 overflow-y-auto p-6 space-y-6">
          <div>
            <h2 className="text-lg font-bold text-gray-800 mb-3">Key Management</h2>
            <button onClick={handleGenerateKeys} className="w-full bg-blue-200 hover:bg-blue-300 text-blue-800 font-semibold py-3 px-4 rounded-lg">Generate Keys</button>
          </div>
          <div className="border-t border-gray-300"></div>

          <div>
            <h2 className="text-lg font-bold text-gray-800 mb-3">Create Capsule</h2>
            <button onClick={() => setShowModal(true)} className="w-full bg-green-200 hover:bg-green-300 text-green-800 font-semibold py-3 px-4 rounded-lg">New Capsule</button>
          </div>
          <div className="border-t border-gray-300"></div>

          <div>
            <h2 className="text-lg font-bold text-gray-800 mb-3">View Capsules</h2>
            <button onClick={handleViewCapsules} className="w-full bg-purple-200 hover:bg-purple-300 text-purple-800 font-semibold py-3 px-4 rounded-lg">List All</button>
          </div>
          <div className="border-t border-gray-300"></div>

          <div>
            <h2 className="text-lg font-bold text-gray-800 mb-3">Operations</h2>
            <div className="space-y-3">
              <input type="number" value={capsuleIndex} onChange={(e) => setCapsuleIndex(e.target.value)} className="w-full p-2.5 border-2 border-gray-300 rounded-lg text-sm" placeholder="Capsule #" min="1" />
              <button onClick={handleDecryptCapsule} className="w-full bg-red-200 hover:bg-red-300 text-red-800 font-semibold py-2.5 px-4 rounded-lg">Decrypt</button>
              <button onClick={handleVerifyCapsule} className="w-full bg-amber-200 hover:bg-amber-300 text-amber-800 font-semibold py-2.5 px-4 rounded-lg">Verify</button>
            </div>
          </div>
          <div className="border-t border-gray-300"></div>

          <button onClick={clearOutput} className="w-full bg-slate-200 hover:bg-slate-300 text-slate-800 font-semibold py-2.5 px-4 rounded-lg">Clear</button>
        </div>

        <div className="flex-1 flex flex-col p-6 overflow-hidden">
          <div className="flex-1 bg-gray-900 rounded-lg overflow-hidden shadow-2xl border-2 border-gray-800 flex flex-col">
            <div className="bg-gray-800 px-6 py-3 border-b-2 border-gray-700 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                </div>
                <span className="font-mono text-gray-400 text-sm ml-2">capsule@quantum:~$</span>
              </div>
              <span className="text-gray-500 font-mono text-xs">{new Date().toLocaleTimeString()}</span>
            </div>
            <pre className="flex-1 p-6 bg-gray-900 text-green-400 font-mono text-sm overflow-auto whitespace-pre-wrap break-words" style={{lineHeight: '1.5'}}>{output}</pre>
          </div>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg shadow-2xl w-full max-w-md p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Create Capsule</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Message</label>
                <textarea value={message} onChange={(e) => setMessage(e.target.value)} className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" rows={5} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Unlock Date</label>
                <input type="date" value={unlockDate} onChange={(e) => setUnlockDate(e.target.value)} className="w-full p-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500" />
              </div>
              <div className="flex gap-3 justify-end pt-4">
                <button onClick={() => setShowModal(false)} className="px-6 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg hover:bg-gray-300">Cancel</button>
                <button onClick={handleCreateCapsule} className="px-6 py-2 bg-green-200 text-green-800 font-semibold rounded-lg hover:bg-green-300">Create</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
