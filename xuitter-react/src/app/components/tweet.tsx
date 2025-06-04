import { useState } from "react";
import { actionTweet, postTweet, TweetAction } from "../api/tweetsApi";

type TweetProps = {
    id: number;
    text: string;
    created_at: string;
    user: string;
    likes_count?: number;
    retweets_count?: number;
    replies_count?: number;
    replies?: TweetProps[];
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
    likes_count = 0,
    retweets_count = 0,
    replies_count = 0,
    replies = [],
    isLiked = false,
    isReposted = false,
    isCommented = false,
    isProfilePageTweet = false,
}: TweetProps) => {
    const [localLikes, setLocalLikes] = useState(likes_count);
    const [localRetweets, setLocalRetweets] = useState(retweets_count);
    const [localReplies, setLocalReplies] = useState(replies_count);
    const [liked, setLiked] = useState(isLiked);
    const [reposted, setReposted] = useState(isReposted);

    // Estados para o modal de reply
    const [showReplyModal, setShowReplyModal] = useState(false);
    const [replyText, setReplyText] = useState("");
    const [replyLoading, setReplyLoading] = useState(false);


    async function handleAction(action: TweetAction) {
        const token = localStorage.getItem("access_token");
        if (!token) {
            alert("Faça login para interagir.");
            return;
        }
        try {
            await actionTweet(id, action, token);
            window.location.reload();
        } catch (err) {
            alert("Erro ao executar ação.");
        }
    }

    async function handleReplySubmit() {
        const token = localStorage.getItem("access_token");
        if (!token || !replyText.trim()) return;
        setReplyLoading(true);
        try {
            await postTweet(replyText, token, id.toString());
            setReplyText("");
            setShowReplyModal(false);
            setLocalReplies((v) => v + 1);
            window.location.reload();
        } catch (err) {
            alert("Erro ao responder.");
        } finally {
            setReplyLoading(false);
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
                    {liked ? "❤️" : "🤍"} {localLikes}
                </button>
                <button onClick={() => handleAction("repost")} className="hover:text-green-500 transition">
                    {reposted ? "🔁" : "🔄"}  {localRetweets}
                </button>
                <button onClick={() => setShowReplyModal(true)} className="hover:text-blue-500 transition">
                    💬 {localReplies}
                </button>
            </div>
            {showReplyModal && (
                <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
                    <div className="bg-white dark:bg-gray-900 p-6 rounded shadow-lg max-w-sm w-full">
                        <h3 className="text-lg font-bold mb-2">Responder para @{user}</h3>
                        <textarea
                            className="w-full border rounded p-2 mb-4"
                            rows={3}
                            placeholder="Digite sua resposta..."
                            value={replyText}
                            onChange={e => setReplyText(e.target.value)}
                            disabled={replyLoading}
                        />
                        <div className="flex justify-end gap-2">
                            <button
                                className="px-4 py-1 rounded bg-gray-200 dark:bg-gray-700"
                                onClick={() => setShowReplyModal(false)}
                                disabled={replyLoading}
                            >
                                Cancelar
                            </button>
                            <button
                                className="px-4 py-1 rounded bg-blue-600 text-white font-semibold"
                                onClick={handleReplySubmit}
                                disabled={replyLoading || !replyText.trim()}
                            >
                                {replyLoading ? "Enviando..." : "Postar"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
            {replies && replies.length > 0 && (
                <div className="ml-6 mt-2 border-l-2 border-gray-200 dark:border-gray-700 pl-4">
                    {replies.map((reply) => (
                        <Tweet key={reply.id} {...reply} />
                    ))}
                </div>
            )}
        </div>


    );
};