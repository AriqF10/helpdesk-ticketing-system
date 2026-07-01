import client from './client';

export const listTickets = (params) => client.get('/tickets/', { params });

export const getTicket = (id) => client.get(`/tickets/${id}/`);

export const createTicket = (payload) => client.post('/tickets/', payload);

export const updateTicket = (id, payload) => client.patch(`/tickets/${id}/`, payload);

export const getDashboard = () => client.get('/tickets/dashboard/');

export const listComments = (ticketId) => client.get(`/tickets/${ticketId}/comments/`);

export const addComment = (ticketId, payload) =>
  client.post(`/tickets/${ticketId}/comments/`, payload);

export const listAttachments = (ticketId) => client.get(`/tickets/${ticketId}/attachments/`);

export const uploadAttachment = (ticketId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return client.post(`/tickets/${ticketId}/attachments/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
