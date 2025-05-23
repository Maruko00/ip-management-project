const API_BASE_URL = "/api"; // Using a relative path, assuming proxy is set up

// Helper function for fetch requests
async function request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    };

    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: response.statusText }));
            throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`);
        }
        if (response.status === 204) { // No Content
            return null;
        }
        return response.json();
    } catch (error) {
        console.error(`API request failed: ${error.message}`, { url, options });
        throw error; // Re-throw to be caught by the caller
    }
}

// Subnet API calls
export const getSubnets = () => request('/subnets');
export const createSubnet = (subnetData) => request('/subnets', { method: 'POST', body: JSON.stringify(subnetData) });
export const updateSubnet = (subnetId, subnetData) => request(`/subnets/${subnetId}`, { method: 'PUT', body: JSON.stringify(subnetData) });
export const deleteSubnet = (subnetId) => request(`/subnets/${subnetId}`, { method: 'DELETE' });

// IP Address API calls
export const getIpAddresses = (subnetId = null, status = null) => {
    const params = new URLSearchParams();
    if (subnetId) params.append('subnet_id', subnetId);
    if (status) params.append('status', status);
    const queryString = params.toString();
    return request(`/ips${queryString ? `?${queryString}` : ''}`);
};
export const createIpAddress = (ipData) => request('/ips', { method: 'POST', body: JSON.stringify(ipData) });
export const updateIpAddress = (ipId, ipData) => request(`/ips/${ipId}`, { method: 'PUT', body: JSON.stringify(ipData) });
export const deleteIpAddress = (ipId) => request(`/ips/${ipId}`, { method: 'DELETE' });
