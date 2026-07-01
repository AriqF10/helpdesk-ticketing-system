import client from './client';

export const listArticles = (params) => client.get('/articles/', { params });

export const getArticle = (id) => client.get(`/articles/${id}/`);

export const createArticle = (payload) => client.post('/articles/', payload);

export const updateArticle = (id, payload) => client.patch(`/articles/${id}/`, payload);

export const deleteArticle = (id) => client.delete(`/articles/${id}/`);
