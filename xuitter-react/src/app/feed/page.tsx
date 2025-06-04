import { useEffect, useState } from "react";
import { Sidebar } from "../components/sidebar";
import { Tweet } from "../components/tweet";
import { fetchFeed, postTweet } from "../api/tweetsApi";

export const Feed = () => {
    const [tweets, setTweets] = useState<any[]>([]);
    const [tweetText, setTweetText] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (!token) {
            window.location.href = "/login";
            return;
        }

        async function fetchTweetsList() {
            const tweets = await fetchFeed(token as string);
            setTweets(tweets);
        }

        fetchTweetsList();
    }, []);

    async function handlePostTweet() {
        const token = localStorage.getItem("access_token");
        if (!token || !tweetText.trim()) return;
        setLoading(true);
        try {
            await postTweet(tweetText, token);
            setTweetText("");
            const tweets = await fetchFeed(token);
            setTweets(tweets);
        } catch (err) {
            alert("Erro ao postar tweet");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="grid grid-cols-[280px_1fr_350px] min-h-screen w-full bg-white text-black dark:bg-black dark:text-white">
            <Sidebar />
            <main className="border-x border-gray-200 dark:border-gray-800 p-4">
                <h1 className="text-xl font-bold mb-4">Home</h1>
                <div className="border-b border-gray-200 dark:border-gray-800 pb-4 mb-4">
                    <textarea
                        placeholder="What's happening?"
                        className="w-full bg-transparent outline-none resize-none text-lg"
                        value={tweetText}
                        onChange={e => setTweetText(e.target.value)}
                        disabled={loading}
                    />
                    <div className="flex justify-end mt-2">
                        <button
                            className="bg-blue-500 text-white px-4 py-1 rounded-full hover:bg-blue-600 disabled:opacity-50"
                            onClick={handlePostTweet}
                            disabled={loading || !tweetText.trim()}
                        >
                            {loading ? "Posting..." : "Post"}
                        </button>
                    </div>
                </div>

                <div className="flex flex-col gap-6">
                    {tweets.map((tweet, idx) => (
                        <Tweet key={idx} {...tweet} />
                    ))}
                </div>
            </main>
        </div>
    );
}