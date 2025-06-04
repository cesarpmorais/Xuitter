export const API_URL = "http://127.0.0.1:8000";

export async function signup(user_data: { username: string; email: string; password: string }) {
    const res = await fetch(`${API_URL}/signup/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(user_data),
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(JSON.stringify(errorData));
    }
    return res.json();
}

export async function login(user_data: { email: string; password: string }) {
    const res = await fetch(`${API_URL}/login/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(user_data),
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(JSON.stringify(errorData));
    }
    return res.json();
}