export const API_URL = "http://127.0.0.1:8000";

export async function fetchFeed(token: string) {
    const res = await fetch(`${API_URL}/post/feed`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(JSON.stringify(errorData));
    }
    return res.json();
}