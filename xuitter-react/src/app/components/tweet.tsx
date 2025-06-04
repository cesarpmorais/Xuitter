import { useState } from "react";
import { actionTweet, TweetAction } from "../api/tweetsApi";

type TweetProps = {
    id: number;
    text: string;
    created_at: string;
    user: string;
    likes?: number;
    retweets?: number;
    replies?: number;
    isLiked?: boolean;
    isReposted?: boolean;
    isCommented?: boolean;
    isProfilePageTweet?: boolean;
};

export const Tweet = ({
    id,
    text,
    created_at,
    user,
    likes = 0,
    retweets = 0,
    replies = 0,
    isLiked = false,
    isReposted = false,
    isCommented = false,
    isProfilePageTweet = false,
}: TweetProps) => {
    const [localLikes, setLocalLikes] = useState(likes);
    const [localRetweets, setLocalRetweets] = useState(retweets);
    const [localReplies, setLocalReplies] = useState(replies);
    const [liked, setLiked] = useState(isLiked);
    const [reposted, setReposted] = useState(isReposted);

    async function handleAction(action: TweetAction) {
        const token = localStorage.getItem("access_token");
        if (!token) {
            alert("Faça login para interagir.");
            return;
        }
        try {
            await actionTweet(id, action, token);
            if (action === "like") {
                setLocalLikes((v) => liked ? v - 1 : v + 1);
                setLiked((prev) => !prev);
            }
            if (action === "repost") {
                setLocalRetweets((v) => reposted ? v - 1 : v + 1);
                setReposted((prev) => !prev);
            }
            if (action === "comment") {
                setLocalReplies((v) => v + 1);
            }
        } catch (err) {
            alert("Erro ao executar ação.");
        }
    }

    return (
        <div className="border-b border-gray-200 dark:border-gray-800 pb-4">
            <div className="flex justify-between items-center mb-1">
                {!isProfilePageTweet && (<div>
                    <p className="font-semibold text-lg">
                        {user}
                    </p>
                </div>)}
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    {new Date(created_at).toLocaleString()}
                </p>
            </div>
            <p className="mb-2">{text}</p>
            <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-300">
                <button onClick={() => handleAction("like")} className="hover:text-red-500 transition">
                    ❤️ {localLikes}
                </button>
                <button onClick={() => handleAction("repost")} className="hover:text-green-500 transition">
                    🔁 {localRetweets}
                </button>
                <button onClick={() => handleAction("comment")} className="hover:text-blue-500 transition">
                    💬 {localReplies}
                </button>
            </div>
        </div>
    );
};