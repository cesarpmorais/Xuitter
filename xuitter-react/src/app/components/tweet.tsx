

type TweetProps = {
    user_handle: string;
    content: string;
    timestamp: string;
    likes: number;
    retweets: number;
    replies: number;
    is_liked: boolean;
    is_retweeted: boolean;
};

export const Tweet = ({
    user_handle,
    content,
    timestamp,
    likes,
    retweets,
    replies,
    is_liked,
    is_retweeted,
}: TweetProps) => {
    return (
        <div className="border-b border-gray-200 dark:border-gray-800 pb-4">
            <p className="font-semibold text-lg">{user_handle}</p>
            <p className="mb-2">{content}</p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                {new Date(timestamp).toLocaleString()}
            </p>
            <div className="flex gap-4 text-sm text-gray-600 dark:text-gray-300">
                <span>
                    ❤️ {likes}
                </span>
                <span>
                    🔁 {retweets}
                </span>
                <span>💬 {replies}</span>
            </div>
        </div>
    );
};
