"use client";

import { Tweet } from "../components/tweet";
import { Sidebar } from "../components/sidebar";
import { fetchFeed } from "../api/tweetsApi";
import { useEffect, useState } from "react";

export default function ProfilePage() {
    const defaultAvatar = "/xuitter_photo.jpg";
    const [username, setUsername] = useState<string | null>(null);
    const [userEmail, setUserEmail] = useState<string | null>(null);
    const [tweets, setTweets] = useState<any[]>([]);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        const name = localStorage.getItem("user_name");
        const email = localStorage.getItem("user_email");
        setUsername(name);
        setUserEmail(email);

        if (!token) {
            window.location.href = "/login";
            return;
        }

        async function fetchTweets() {
            const tweets = await fetchFeed(token as string);
            const userTweets = tweets.filter((tweet: { user: string | null; }) => tweet.user === name);
            setTweets(userTweets);
        }

        if (name) {
            fetchTweets();
        }
    }, []);

    return (
        <div className="grid grid-cols-[280px_1fr_350px] min-h-screen w-full bg-white text-black dark:bg-black dark:text-white">
            <Sidebar />
            <main className="border-x border-gray-200 dark:border-gray-800">
                {/* Banner */}
                <div
                    className="h-40 w-full bg-cover bg-center"
                    style={{ backgroundColor: "#3b94da" }}
                />
                {/* Avatar e infos */}
                <div className="relative px-6">
                    <img
                        src={defaultAvatar}
                        className="w-24 h-24 aspect-square object-cover rounded-full border-4 border-white dark:border-black absolute -top-12 left-6"
                    />
                    <div className="pl-32 pt-4 pb-2">
                        <h2 className="text-2xl font-bold">{username}</h2>
                        <div className="text-gray-500">{userEmail}</div>
                    </div>
                </div>
                {/* Divider */}
                <div className="border-b border-gray-200 dark:border-gray-800 my-2" />
                {/* Tweets */}
                <div className="flex flex-col gap-6 p-6">
                    {tweets.length > 0 ? (
                        tweets.map((tweet: any, index: number) => (
                            <Tweet key={index} isProfilePageTweet={true} {...tweet} />
                        ))
                    ) : (
                        <div className="text-center text-gray-500">Nenhum tweet ainda.</div>
                    )}
                </div>
            </main>
        </div>
    );
}