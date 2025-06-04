"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Sidebar } from "./components/sidebar";
import { Feed } from "./components/feed";

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="grid grid-cols-[280px_1fr_350px] min-h-screen w-full bg-white text-black dark:bg-black dark:text-white">
      <Sidebar />
      <Feed />
    </div>
  );
}