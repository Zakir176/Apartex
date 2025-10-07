import apiClient from './index';

export async function uploadImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  const resp = await apiClient.post('/upload/images', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return resp.data; // { url }
}


