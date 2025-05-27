// app/page.tsx or app/page.jsx

import { Feed } from "./components/feed";
import { Sidebar } from "./components/sidebar";

export default function Home() {
  return (
    <div className="grid grid-cols-[280px_1fr_350px] min-h-screen w-full bg-white text-black dark:bg-black dark:text-white">
      <Sidebar />
      <Feed />
    </div>
  );
}
