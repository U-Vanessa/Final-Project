import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Bell, User, Calendar, FileText, Upload } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import './voucherpage.css';
import UnifiedSidebar from '../components/layout/UnifiedSidebar';
import { documentAPI, usersAPI, voucherAPI } from '../services/api';
import { useThemeMode } from '../contexts/ThemeContext';

const VoucherPage = () => {
  const [formData, setFormData] = useState({
    title: '',
    priority: 'medium',
    problemDescription: ''
  });
  const [activeTab, setActiveTab] = useState('create');
  const [tickets, setTickets] = useState([]);
  const [itPersonnel, setItPersonnel] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = React.useRef(null);
  const location = useLocation();
  const [assignmentState, setAssignmentState] = useState({});
  const [notesState, setNotesState] = useState({});
  const [documentLinkState, setDocumentLinkState] = useState({});
  const { darkMode, toggleDarkMode } = useThemeMode();

  const currentUser = useMemo(() => {
    try {
      return JSON.parse(localStorage.getItem('user') || '{}');
    } catch {
      return {};
    }
  }, []);

  const normalizedRole = (currentUser?.role || '').toLowerCase();
  const isITRole = ['admin', 'manager', 'it'].includes(normalizedRole);
  const canManageTickets = isITRole;
  const canCreateVoucher = !isITRole;
  const currentUserId = Number(currentUser?.id || 0);

  const showOnlyMyTickets = useMemo(() => {
    const searchParams = new URLSearchParams(location.search);
    return searchParams.get('filter') === 'my-tickets';
  }, [location.search]);

  const loadTickets = useCallback(async () => {
    try {
      setLoading(true);

      const voucherParams = {};
      if ((isITRole && currentUserId) || showOnlyMyTickets) {
        voucherParams.assigned_to_id = currentUserId;
      }

      const [voucherData, itData, documentData] = await Promise.all([
        voucherAPI.list(voucherParams),
        usersAPI.listITPersonnel(),
        documentAPI.list(),
      ]);

      const normalizedTickets = (voucherData || []).filter((ticket) => {
        if (normalizedRole === 'user' && currentUserId) {
          return ticket.requester_id === currentUserId;
        }
        return true;
      });
      setTickets(normalizedTickets);
      setItPersonnel(itData || []);
      setDocuments(documentData || []);

      const nextAssignmentState = {};
      const nextNotesState = {};
      const nextDocumentLinkState = {};

      normalizedTickets.forEach((ticket) => {
        nextAssignmentState[ticket.id] = ticket.assigned_to_id || '';
        nextNotesState[ticket.id] = {
          diagnosis: ticket.diagnosis || '',
          action_taken: ticket.action_taken || '',
        };

        const linkedDocument = (documentData || []).find((doc) => doc.voucher_id === ticket.id);
        nextDocumentLinkState[ticket.id] = linkedDocument ? linkedDocument.id : '';
      });

      setAssignmentState(nextAssignmentState);
      setNotesState(nextNotesState);
      setDocumentLinkState(nextDocumentLinkState);
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to load vouchers');
    } finally {
      setLoading(false);
    }
  }, [currentUserId, isITRole, normalizedRole, showOnlyMyTickets]);

  useEffect(() => {
    if (!canCreateVoucher && activeTab === 'create') {
      setActiveTab('list');
    }
  }, [activeTab, canCreateVoucher]);

  useEffect(() => {
    loadTickets();
  }, [loadTickets]);

  const handleFileSelect = (files) => {
    const fileArray = Array.from(files);
    const validFiles = fileArray.filter(file => {
      const validTypes = ['image/png', 'image/jpeg', 'application/pdf'];
      const maxSize = 10 * 1024 * 1024; // 10MB
      return validTypes.includes(file.type) && file.size <= maxSize;
    });

    if (validFiles.length !== fileArray.length) {
      setMessage('Some files were skipped (must be PNG, JPG, or PDF, max 10MB each)');
    }

    setUploadedFiles(prev => [...prev, ...validFiles]);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileInputChange = (e) => {
    handleFileSelect(e.target.files);
  };

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    handleFileSelect(e.dataTransfer.files);
  };

  const getAssigneeLabel = (assignedToId) => {
    if (!assignedToId) {
      return 'Unassigned';
    }

    const match = itPersonnel.find((person) => person.id === assignedToId);
    return match?.full_name || match?.email || `IT #${assignedToId}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!currentUser?.email) {
      setMessage('Please login again to submit voucher.');
      return;
    }

    try {
      setSubmitting(true);
      await voucherAPI.create({
        title: formData.title,
        description: formData.problemDescription,
        priority: formData.priority,
        requester_email: currentUser.email,
      });

      setFormData({
        title: '',
        priority: 'medium',
        problemDescription: '',
      });
      setUploadedFiles([]);
      setMessage('Voucher submitted successfully.');
      await loadTickets();
      setActiveTab('list');
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to submit voucher');
    } finally {
      setSubmitting(false);
    }
  };

  const handleStatusChange = async (ticketId, nextStatus) => {
    try {
      await voucherAPI.update(ticketId, { status: nextStatus });
      setMessage('Ticket status updated.');
      await loadTickets();
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to update ticket status');
    }
  };

  const handleAssign = async (ticketId) => {
    try {
      const assignedTo = assignmentState[ticketId] ? Number(assignmentState[ticketId]) : null;
      await voucherAPI.update(ticketId, {
        assigned_to_id: assignedTo,
        status: assignedTo ? 'assigned' : 'open',
      });
      setMessage('Ticket assignment updated.');
      await loadTickets();
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to update assignment');
    }
  };

  const handleSaveNotes = async (ticketId) => {
    try {
      const payload = notesState[ticketId] || {};
      await voucherAPI.update(ticketId, {
        diagnosis: payload.diagnosis || null,
        action_taken: payload.action_taken || null,
      });
      setMessage('Diagnosis and action saved.');
      await loadTickets();
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to save diagnosis/action');
    }
  };

  const handleLinkDocument = async (ticketId) => {
    try {
      const selectedDocumentId = documentLinkState[ticketId] ? Number(documentLinkState[ticketId]) : null;
      if (!selectedDocumentId) {
        setMessage('Select a document to link.');
        return;
      }

      await documentAPI.linkToVoucher(selectedDocumentId, ticketId);
      setMessage('Document linked to ticket successfully.');
      await loadTickets();
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to link document');
    }
  };

  return (
    <div className="voucher-container">
      <UnifiedSidebar activePath="/voucher" />

      {/* Main Content */}
      <main className="voucher-main">
        <header className="voucher-header">
          <div>
            <h1>Voucher</h1>
            <p>Submit your technical support requests</p>
          </div>
          <div className="voucher-header-right">
            <button className="voucher-icon-btn" type="button" title="Toggle dark mode" onClick={toggleDarkMode}>
              {darkMode ? '☀️' : '🌙'}
            </button>
            <button className="voucher-icon-btn">
              <Bell size={20} />
            </button>
            <div className="voucher-user">
              <User size={20} />
            </div>
          </div>
        </header>

        <div className="voucher-tabs">
          {canCreateVoucher && (
            <button
              className={`voucher-tab ${activeTab === 'create' ? 'active' : ''}`}
              onClick={() => setActiveTab('create')}
            >
              <Calendar size={20} /> Book Appointment
            </button>
          )}
          <button
            className={`voucher-tab ${activeTab === 'list' ? 'active' : ''}`}
            onClick={() => setActiveTab('list')}
          >
            <FileText size={20} /> {canCreateVoucher ? 'View Requests' : 'My Assigned Requests'}
          </button>
        </div>

        {message && <div className="voucher-message">{message}</div>}

        {canCreateVoucher && activeTab === 'create' && <div className="voucher-form-container">
          <h2>Submit New Voucher</h2>
          <p>Fill in the details below to create a support ticket</p>

          <form onSubmit={handleSubmit}>
            <div className="voucher-form-group">
              <label>Name *</label>
              <input
                type="text"
                placeholder="Enter issue title"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
            </div>

            <div className="voucher-form-group">
              <label>Category *</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                required
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>

            <div className="voucher-form-group">
              <label>Problem Description *</label>
              <textarea
                placeholder="Describe your issue in detail..."
                value={formData.problemDescription}
                onChange={(e) => setFormData({ ...formData, problemDescription: e.target.value })}
                rows="6"
                required
              />
              <small>{formData.problemDescription.length} characters</small>
            </div>

            <div className="voucher-form-group voucher-upload-group">
              <label>Attachments (Optional)</label>
              <div 
                className="voucher-upload"
                onClick={handleUploadClick}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                style={{ cursor: 'pointer' }}
              >
                <Upload size={24} />
                <p>Click to upload or drag and drop</p>
                <small>PNG, JPG, PDF up to 10MB</small>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".png,.jpg,.jpeg,.pdf"
                onChange={handleFileInputChange}
                style={{ display: 'none' }}
              />
              {uploadedFiles.length > 0 && (
                <div style={{ marginTop: '12px' }}>
                  <p style={{ fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
                    Selected files ({uploadedFiles.length}):
                  </p>
                  <ul style={{ listStyle: 'none', padding: 0 }}>
                    {uploadedFiles.map((file, index) => (
                      <li key={index} style={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center',
                        padding: '8px',
                        backgroundColor: '#f0f2f5',
                        borderRadius: '6px',
                        marginBottom: '6px',
                        fontSize: '14px'
                      }}>
                        <span>{file.name}</span>
                        <button
                          type="button"
                          onClick={() => removeFile(index)}
                          style={{ 
                            background: 'none', 
                            border: 'none', 
                            color: '#e74c3c',
                            cursor: 'pointer',
                            fontSize: '16px'
                          }}
                        >
                          ✕
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <button type="submit" className="voucher-submit-btn">
              {submitting ? 'Submitting...' : 'Submit Voucher'}
            </button>
          </form>
        </div>}

        {activeTab === 'list' && (
          <div className="voucher-form-container">
            <h2>Submitted Vouchers</h2>
            <p>Monitor and update ticket progress</p>

            {loading && <p>Loading vouchers...</p>}

            {!loading && tickets.length === 0 && (
              <p>{(showOnlyMyTickets || isITRole) ? 'No tickets currently assigned to you.' : 'No vouchers found.'}</p>
            )}

            {!loading && tickets.length > 0 && (
              <div className="voucher-ticket-grid">
                {tickets.map((ticket) => (
                  <div key={ticket.id} className="voucher-ticket-card">
                    <h4>{ticket.ticket_number} • {ticket.title}</h4>
                    <p>{ticket.description}</p>
                    <p>Priority: <strong>{ticket.priority}</strong> | Status: <strong>{ticket.status}</strong></p>
                    <p>
                      Assigned To: <strong>{getAssigneeLabel(ticket.assigned_to_id)}</strong>
                    </p>

                    {canManageTickets && (
                      <div className="voucher-ticket-actions-row">
                        <button className="voucher-ticket-action" type="button" onClick={() => handleStatusChange(ticket.id, 'in_progress')}>
                          Mark In Progress
                        </button>
                        <button className="voucher-ticket-action" type="button" onClick={() => handleStatusChange(ticket.id, 'resolved')}>
                          Mark Resolved
                        </button>
                        <button className="voucher-ticket-action voucher-ticket-action-danger" type="button" onClick={() => handleStatusChange(ticket.id, 'closed')}>
                          Close
                        </button>
                      </div>
                    )}

                    {canManageTickets && (
                      <div className="voucher-ticket-manage">
                        <div className="voucher-ticket-inline">
                          <label className="voucher-ticket-label">Assign IT:</label>
                          <select
                            className="voucher-ticket-select"
                            value={assignmentState[ticket.id] || ''}
                            onChange={(e) => setAssignmentState((prev) => ({ ...prev, [ticket.id]: e.target.value }))}
                          >
                            <option value="">Unassigned</option>
                            {itPersonnel.map((person) => (
                              <option key={person.id} value={person.id}>
                                {person.full_name || person.email}
                              </option>
                            ))}
                          </select>
                          <button className="voucher-ticket-action" type="button" onClick={() => handleAssign(ticket.id)}>Save Assignment</button>
                        </div>

                        <div className="voucher-ticket-notes">
                          <label className="voucher-ticket-label">Diagnosis</label>
                          <textarea
                            className="voucher-ticket-textarea"
                            rows="2"
                            value={notesState[ticket.id]?.diagnosis || ''}
                            onChange={(e) =>
                              setNotesState((prev) => ({
                                ...prev,
                                [ticket.id]: {
                                  diagnosis: e.target.value,
                                  action_taken: prev[ticket.id]?.action_taken || '',
                                },
                              }))
                            }
                          />

                          <label className="voucher-ticket-label">Action Taken</label>
                          <textarea
                            className="voucher-ticket-textarea"
                            rows="2"
                            value={notesState[ticket.id]?.action_taken || ''}
                            onChange={(e) =>
                              setNotesState((prev) => ({
                                ...prev,
                                [ticket.id]: {
                                  diagnosis: prev[ticket.id]?.diagnosis || '',
                                  action_taken: e.target.value,
                                },
                              }))
                            }
                          />
                          <button className="voucher-ticket-action" type="button" onClick={() => handleSaveNotes(ticket.id)}>Save Diagnosis/Action</button>
                        </div>

                        <div className="voucher-ticket-inline">
                          <label className="voucher-ticket-label">Link Document:</label>
                          <select
                            className="voucher-ticket-select"
                            value={documentLinkState[ticket.id] || ''}
                            onChange={(e) => setDocumentLinkState((prev) => ({ ...prev, [ticket.id]: e.target.value }))}
                          >
                            <option value="">Select document</option>
                            {documents.map((doc) => (
                              <option key={doc.id} value={doc.id}>
                                {doc.document_ref} - {doc.name_of_staff}
                              </option>
                            ))}
                          </select>
                          <button className="voucher-ticket-action" type="button" onClick={() => handleLinkDocument(ticket.id)}>Link</button>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <footer className="voucher-footer">©2026. ASM</footer>
      </main>
    </div>
  );
};

export default VoucherPage;