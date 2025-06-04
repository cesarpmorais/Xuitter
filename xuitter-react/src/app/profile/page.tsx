"use client";

import { Tweet } from "../components/tweet";
import { Sidebar } from "../components/sidebar";
import { fetchFeed } from "../api/tweetsApi";
import { useEffect, useState } from "react";
import { logout } from "../api/userApi";

export default function ProfilePage() {
    const defaultAvatar = "/xuitter_photo.jpg";
    const [username, setUsername] = useState<string | null>(null);
    const [userEmail, setUserEmail] = useState<string | null>(null);
    const [tweets, setTweets] = useState<any[]>([]);
    const [showModal, setShowModal] = useState(false);

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

    async function handleLogout() {
        await logout(
            localStorage.getItem("access_token") || "",
            localStorage.getItem("refresh_token") || ""
        );
        localStorage.clear();
        window.location.href = "/login";
    }

    return (
        <div className="grid grid-cols-[280px_1fr_350px] min-h-screen w-full bg-white text-black dark:bg-black dark:text-white">
            <Sidebar />
            <main className="border-x border-gray-200 dark:border-gray-800">
                {/* Banner */}
                <div className="h-40 w-full bg-cover bg-center" style={{ backgroundColor: "#3b94da" }} />
                {/* Avatar e infos + Logout */}
                <div className="relative px-6 flex items-start justify-between">
                    <div className="flex-1">
                        <img
                            src={defaultAvatar}
                            className="w-24 h-24 aspect-square object-cover rounded-full border-4 border-white dark:border-black absolute -top-12 left-6"
                        />
                        <div className="pl-32 pt-4 pb-2">
                            <h2 className="text-2xl font-bold">{username}</h2>
                            <div className="text-gray-500">{userEmail}</div>
                        </div>
                    </div>
                    <button
                        className="mt-4 ml-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded font-semibold"
                        onClick={() => setShowModal(true)}
                    >
                        Log out
                    </button>
                </div>
                {/* Modal */}
                {showModal && (
                    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
                        <div className="bg-white dark:bg-gray-900 p-6 rounded shadow-lg max-w-sm w-full">
                            <h3 className="text-lg font-bold mb-2">Confirm logout</h3>
                            <p className="mb-4">Are you sure you want to log out?</p>
                            <div className="flex justify-end gap-2">
                                <button
                                    className="px-4 py-1 rounded bg-gray-200 dark:bg-gray-700"
                                    onClick={() => setShowModal(false)}
                                >
                                    Cancel
                                </button>
                                <button
                                    className="px-4 py-1 rounded bg-red-600 text-white font-semibold"
                                    onClick={handleLogout}
                                >
                                    Log out
                                </button>
                            </div>
                        </div>
                    </div>
                )}
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