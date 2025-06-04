export const API_URL = "http://127.0.0.1:8000";
export type TweetAction = "like" | "repost" | "comment";

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

export async function postTweet(message: string, token: string, origin?: string) {
    const res = await fetch(`${API_URL}/post/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ "text": message, "origin": origin }),
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(JSON.stringify(errorData));
    }
    return res.json();
}

export async function actionTweet(postPK: number, action: TweetAction, token: string,) {
    const res = await fetch(`${API_URL}/post/${postPK}/action/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ "action": action }),
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(JSON.stringify(errorData));
    }
    return res.json();
}