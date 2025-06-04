type TweetProps = {
    id: number;
    text: string;
    created_at: string;
    user: string;
    likes?: number;
    retweets?: number;
    replies?: number;
};

export const Tweet = ({
    id,
    text,
    created_at,
    user,
    likes = 0,
    retweets = 0,
    replies = 0,
}: TweetProps) => {
    return (
        <div className="border-b border-gray-200 dark:border-gray-800 pb-4">
            <div className="flex justify-between items-center mb-1">
                <div>
                    <p className="font-semibold text-lg">
                        {user}
                    </p>
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    {new Date(created_at).toLocaleString()}
                </p>
            </div>
            <p className="mb-2">{text}</p>
            <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-300">
                <span>❤️ {likes}</span>
                <span>🔁 {retweets}</span>
                <span>💬 {replies}</span>
            </div>
        </div>
    );
};