const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchWithAuth(url: string, options: RequestInit = {}) {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string>),
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(`${API_URL}${url}`, { ...options, headers });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response;
}


export async function login(username: string, password: string) {
    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username, password }),
    });
    if (!response.ok) {
        throw new Error('Login failed');
    }
    const data = await response.json();
    if (typeof window !== 'undefined') {
        localStorage.setItem('token', data.access_token);
    }
    return data;
}

export async function getYears() {
    try {
        const response = await fetchWithAuth('/years')
        return await response.json();
    } catch (error) {
        console.error('Error in getYears:', error)
        return []
    }
}

export async function createYear(yearData: { year: number }) {
    const response = await fetchWithAuth('/years', {
        method: 'POST',
        body: JSON.stringify(yearData),
    })
    return response.json()
}

export async function getEntries(yearId: number) {
    const response = await fetchWithAuth(`/years/${yearId}/entries`)
    return response.json()
}

export async function createEntry(payload: {
    revenue: number;
    cost: number;
    date: number;
    year_id: number;
    cat_id: number;
    file_id: number | null;
}) {
    const token = localStorage.getItem('token');

    const response = await fetch(`${API_URL}/years/${payload.year_id}/entries`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json();
        console.error('Error response from backend:', errorData);
        throw new Error(`HTTP error! status: ${response.status}`);
    }


    return response.json();
}


export async function getProfit(yearId: number) {
    const response = await fetchWithAuth(`/years/${yearId}/profit`)
    return response.json()
}

export async function getCategories() {
    const response = await fetchWithAuth('/categories');
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.data;
}

export async function downloadFile(fileId: number) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_URL}/years/uploads/${fileId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `file_${fileId}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}



export async function uploadFile(file: File): Promise<number> {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/years/uploads`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    // Return file_id
    return data.data.id;
}


export async function exportCsv(yearId: number) {
    const response = await fetchWithAuth(`/years/${yearId}/export/csv`, {
        headers: {
            'Accept': 'text/csv',
        },
    })
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.style.display = 'none'
    a.href = url
    a.download = `year_${yearId}_export.csv`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
}

export async function exportPdf(yearId: number) {
    const response = await fetchWithAuth(`/years/${yearId}/export/pdf`, {
        headers: {
            'Accept': 'application/pdf',
        },
    })
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.style.display = 'none'
    a.href = url
    a.download = `year_${yearId}_export.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
}

