import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:5000';

function App() {
  const [output, setOutput] = useState('Welcome to Quantum-Safe Digital Time Capsule!\nUse the buttons below to interact with the application.\n\n');
  const [message, setMessage] = useState('');
  const [unlockDate, setUnlockDate] = useState('');
  const [capsuleIndex, setCapsuleIndex] = useState('');
  const [showModal, setShowModal] = useState(false);

  const appendOutput = (text: string) => {
    setOutput(prev => prev + text);
  };

  const clearOutput = () => {
    setOutput('');
  };

  const handleGenerateKeys = async () => {
    try {
      const response = await axios.post(`${API_BASE}/generate_keys`);
      if (response.data.success) {
        appendOutput('✅ PQC Keys generated and saved!\n\n');
      } else {
        appendOutput(`❌ Error: ${response.data.error}\n\n`);
      }
    } catch (error) {
      appendOutput(`❌ Error generating keys: ${error}\n\n`);
    }
  };

  const openCreateModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };
  
  const handleCreateCapsule = async () => {
    if (!message.trim()) {
      appendOutput('❌ Message cannot be empty.\n\n');
      return;
    }
    if (!unlockDate) {
      appendOutput('❌ Unlock date cannot be empty.\n\n');
      return;
    }
    try {
      const response = await axios.post(`${API_BASE}/create_capsule`, {
        message: message.trim(),
        unlock_date: unlockDate
      });
      if (response.data.success) {
        appendOutput(`🔒 ${response.data.message}\n\n`);
        setMessage('');
        setUnlockDate('');
        closeModal();
      } else {
        appendOutput(`❌ Error: ${response.data.error}\n\n`);
      }
    } catch (error) {
      appendOutput(`❌ Error creating capsule: ${error}\n\n`);
    }
  };

  const handleViewCapsules = async () => {
    try {
      const response = await axios.get(`${API_BASE}/capsules`);
      if (response.data.success) {
        const capsules = response.data.capsules;
        if (capsules.length === 0) {
          appendOutput('📭 No capsules found.\n\n');
        } else {
          appendOutput('📦 Available Capsules:\n');
          capsules.forEach((cap: any, index: number) => {
            const status = cap.status === 'unlocked' ? '🔓 Unlocked' : '🔒 Locked';
            appendOutput(`${index + 1}. ${cap.timestamp} - Unlock: ${cap.unlock_date} (${status})\n`);
          });
          appendOutput('\n');
        }
      } else {
        appendOutput(`❌ Error: ${response.data.error}\n\n`);
      }
    } catch (error) {
      appendOutput(`❌ Error viewing capsules: ${error}\n\n`);
    }
  };

  const handleDecryptCapsule = async () => {
    const index = parseInt(capsuleIndex);
    if (isNaN(index) || index < 1) {
      appendOutput('❌ Invalid capsule index. Please enter a valid number.\n\n');
      return;
    }
    try {
      const response = await axios.post(`${API_BASE}/decrypt_capsule`, {
        capsule_index: index - 1
      });
      if (response.data.success) {
        appendOutput(`${response.data.message}\n`);
        appendOutput(`📬 Decrypted Message:\n${response.data.decrypted_message}\n\n`);
        appendOutput(`⏰ Timestamp: ${response.data.timestamp}\n`);
        appendOutput(`📅 Unlock Date: ${response.data.unlock_date}\n`);
        appendOutput(`✅ Signature verified - Capsule is authentic!\n\n`);
        setCapsuleIndex('');
      } else {
        appendOutput(`❌ Error: ${response.data.error}\n\n`);
      }
    } catch (error: any) {
      appendOutput(`❌ Error decrypting capsule: ${error.message || error}\n\n`);
    }
  };

  const handleVerifyCapsule = async () => {
    const index = parseInt(capsuleIndex);
    if (isNaN(index) || index < 1) {
      appendOutput('❌ Invalid capsule index. Please enter a valid number.\n\n');
      return;
    }
    try {
      const response = await axios.post(`${API_BASE}/verify_capsule`, {
        capsule_index: index - 1
      });
      if (response.data.success) {
        appendOutput(`${response.data.message}\n\n`);
        appendOutput(`⏰ Timestamp: ${response.data.timestamp}\n`);
        appendOutput(`📅 Unlock Date: ${response.data.unlock_date}\n`);
        appendOutput(`Verified: ${response.data.verified ? '✅ Yes' : '❌ No'}\n\n`);
        setCapsuleIndex('');
      } else {
        appendOutput(`❌ Error: ${response.data.error}\n\n`);
      }
    } catch (error: any) {
      appendOutput(`❌ Error verifying capsule: ${error.message || error}\n\n`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-8 card">
        <div className="flex items-center justify-center mb-8">
          <div className="mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-center text-blue-800 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
            Quantum-Safe Digital Time Capsule
          </h1>
        </div>

        {/* Buttons */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          <button
            onClick={handleGenerateKeys}
            className="bg-gradient-to-r from-blue-500 to-blue-700 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:shadow-lg btn-glow flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
            Generate Keys
          </button>
          <button
            onClick={openCreateModal}
            className="bg-gradient-to-r from-green-500 to-green-700 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:shadow-lg btn-glow flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Create Capsule
          </button>
          <button
            onClick={handleViewCapsules}
            className="bg-gradient-to-r from-purple-500 to-purple-700 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:shadow-lg btn-glow flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            View Capsules
          </button>
          <button
            onClick={handleDecryptCapsule}
            className="bg-gradient-to-r from-red-500 to-red-700 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:shadow-lg btn-glow flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z" />
            </svg>
            Decrypt Capsule
          </button>
          <button
            onClick={handleVerifyCapsule}
            className="bg-gradient-to-r from-yellow-500 to-yellow-700 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:shadow-lg btn-glow flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            Verify Capsule
          </button>
          <button
            onClick={clearOutput}
            className="bg-gradient-to-r from-gray-500 to-gray-700 text-white font-bold py-3 px-4 rounded-lg shadow-md hover:shadow-lg btn-glow flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Clear Output
          </button>
        </div>

        {/* Inputs - Only Capsule Index */}
        <div className="mb-6">
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 shadow-inner">
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
              </svg>
              Capsule Index (for decrypt/verify):
            </label>
            <div className="relative">
              <input
                type="number"
                value={capsuleIndex}
                onChange={(e) => setCapsuleIndex(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 pl-10"
                placeholder="Enter capsule number..."
                min="1"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-gray-500">#</span>
              </div>
            </div>
            <p className="mt-1 text-xs text-gray-500 italic">Enter the number of the capsule you want to decrypt or verify</p>
          </div>
        </div>
        
        {/* Create Capsule Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg p-8 border border-gray-300 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-start mb-8">
                <h2 className="text-2xl font-bold text-green-600 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 mr-3 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Create New Time Capsule
                </h2>
                <button 
                  onClick={closeModal}
                  className="text-gray-500 hover:text-gray-700 transition-colors focus:outline-none"
                  aria-label="Close"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-800 mb-3 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                    </svg>
                    Message for Capsule:
                  </label>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    rows={5}
                    placeholder="Enter your message..."
                  />
                  <p className="mt-2 text-xs text-gray-600">This message will be encrypted with quantum-safe encryption</p>
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-800 mb-3 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Unlock Date (YYYY-MM-DD):
                  </label>
                  <input
                    type="date"
                    value={unlockDate}
                    onChange={(e) => setUnlockDate(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  />
                  <p className="mt-2 text-xs text-gray-600">The capsule can only be decrypted after this date</p>
                </div>
                
                <div className="flex gap-3 justify-end">
                  <button 
                    onClick={closeModal}
                    className="px-6 py-2 bg-gray-200 text-gray-800 font-medium rounded-lg hover:bg-gray-300 transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    onClick={handleCreateCapsule}
                    className="px-6 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                    Create Capsule
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Output */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="block text-sm font-medium text-gray-700 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Terminal Output:
            </label>
            <div className="flex space-x-1">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
          </div>
          <div className="bg-gray-900 rounded-lg overflow-hidden shadow-lg border border-gray-700">
            <div className="bg-gray-800 px-4 py-2 text-xs text-gray-400 flex justify-between items-center">
              <span>quantum-capsule@terminal:~$</span>
              <span>{new Date().toLocaleString()}</span>
            </div>
            <textarea
              value={output}
              readOnly
              className="w-full p-4 bg-gray-900 text-green-400 font-mono text-sm"
              rows={15}
              style={{ outline: 'none', resize: 'vertical' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
