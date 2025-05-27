import initial_tweets from "../utils/initial_tweets.json";
import { Tweet } from "./tweet";

export const Feed = () => {
    return (
        <main className="border-x border-gray-200 dark:border-gray-800 p-4">
            <h1 className="text-xl font-bold mb-4">Home</h1>
            <div className="border-b border-gray-200 dark:border-gray-800 pb-4 mb-4">
                <textarea
                    placeholder="What's happening?"
                    className="w-full bg-transparent outline-none resize-none text-lg"
                />
                <div className="flex justify-end mt-2">
                    <button className="bg-blue-500 text-white px-4 py-1 rounded-full hover:bg-blue-600">
                        Post
                    </button>
                </div>
            </div>

            <div className="flex flex-col gap-6">
                {initial_tweets.map((tweet: any, index: any) => (
                    <Tweet key={index} {...tweet} />
                ))}
            </div>
        </main>
    );
}