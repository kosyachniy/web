import { api } from './client';

export interface LoginRequest {
    email: string;
    password: string;
}

export interface LoginResponse {
    token: string;
    user: {
        id: number;
        email: string;
        name: string;
    };
}

export interface RegisterRequest {
    email: string;
    password: string;
    name: string;
}

export interface User {
    id: number;
    email: string;
    name: string;
    createdAt: string;
    updatedAt: string;
}

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/login/', credentials);
    
    // Store token in localStorage
    if (typeof window !== 'undefined' && response.token) {
        localStorage.setItem('authToken', response.token);
    }
    
    return response;
}

export async function register(userData: RegisterRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>('/auth/register/', userData);
    
    // Store token in localStorage
    if (typeof window !== 'undefined' && response.token) {
        localStorage.setItem('authToken', response.token);
    }
    
    return response;
}

export async function logout(): Promise<void> {
    try {
        await api.post('/auth/logout/');
    } finally {
        // Always clear token from localStorage
        if (typeof window !== 'undefined') {
            localStorage.removeItem('authToken');
        }
    }
}

export async function getCurrentUser(): Promise<User> {
    return api.get<User>('/auth/me/');
}

export async function refreshToken(): Promise<LoginResponse> {
    return api.post<LoginResponse>('/auth/refresh/');
}

export async function forgotPassword(email: string): Promise<void> {
    return api.post('/auth/forgot-password/', { email });
}

export async function resetPassword(token: string, password: string): Promise<void> {
    return api.post('/auth/reset-password/', { token, password });
}