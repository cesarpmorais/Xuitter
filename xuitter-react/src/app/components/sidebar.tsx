"use client";
import { useRouter } from "next/navigation";

export const Sidebar = () => {
    const router = useRouter();

    return (
        <aside className="w-48 p-2 border-r border-gray-200 dark:border-gray-800 sticky top-0 h-screen">
            <div className="text-lg font-bold mb-6 cursor-pointer text-center"
                onClick={() => router.push("/")}>
                Xuitter
            </div>
            <nav className="flex flex-col gap-3">
                <button
                    className="hover:bg-gray-100 dark:hover:bg-gray-800 p-1.5 rounded text-sm"
                    onClick={() => router.push("/")}
                >
                    Home
                </button>
                <button
                    className="hover:bg-gray-100 dark:hover:bg-gray-800 p-1.5 rounded text-sm"
                    onClick={() => router.push("/profile")}
                >
                    Profile
                </button>
            </nav>
        </aside>
    );
};
