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


export async function logout(access_token: string, refresh_token: string) {
    const res = await fetch(`${API_URL}/logout/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
        },
        body: JSON.stringify({ refresh: refresh_token }),
    });

    if (!res.ok) {
        let errorData;
        try {
            errorData = await res.json();
        } catch {
            errorData = { detail: "Erro desconhecido no logout." };
        }
        throw new Error(JSON.stringify(errorData));
    }

    if (res.status === 204 || res.status === 205) {
        return { detail: "Logout successful." };
    }
    return res.json();
}