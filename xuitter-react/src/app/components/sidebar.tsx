export const Sidebar = () => {
    return (
        <aside className="w-48 p-2 border-r border-gray-200 dark:border-gray-800 sticky top-0 h-screen">
            <div className="text-lg font-bold mb-6">Xuitter</div>
            <nav className="flex flex-col gap-3">
                <button className="hover:bg-gray-100 dark:hover:bg-gray-800 p-1.5 rounded text-sm">
                    Home
                </button>
                <button className="hover:bg-gray-100 dark:hover:bg-gray-800 p-1.5 rounded text-sm">
                    Profile
                </button>
            </nav>
        </aside>
    );
};
