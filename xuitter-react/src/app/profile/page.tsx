import initial_tweets from "../utils/initial_tweets.json";
import { Tweet } from "../components/tweet";
import { Sidebar } from "../components/sidebar";

export default function ProfilePage() {
    const defaultAvatar = "/xuitter_photo.jpg";
    // Simulação de dados do usuário
    const user = {
        name: "Cesar",
        username: "cesar_dev",
        bio: "Desenvolvedor apaixonado por tecnologia.",
        avatar: "/xuitter_photo.jpg",
    };

    // Filtra tweets do usuário (ajuste conforme sua estrutura real)
    const userTweets = initial_tweets.filter(
        (tweet: any) => tweet.username === user.username
    );

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
                        alt={user.name}
                        className="w-24 h-24 aspect-square object-cover rounded-full border-4 border-white dark:border-black absolute -top-12 left-6"
                    />
                    <div className="pl-32 pt-4 pb-2">
                        <h2 className="text-2xl font-bold">{user.name}</h2>
                        <div className="text-gray-500">@{user.username}</div>
                        <div className="mt-2">{user.bio}</div>
                    </div>
                </div>
                {/* Divider */}
                <div className="border-b border-gray-200 dark:border-gray-800 my-2" />
                {/* Tweets */}
                <div className="flex flex-col gap-6 p-6">
                    {userTweets.length > 0 ? (
                        userTweets.map((tweet: any, index: number) => (
                            <Tweet key={index} {...tweet} />
                        ))
                    ) : (
                        <div className="text-center text-gray-500">Nenhum tweet ainda.</div>
                    )}
                </div>
            </main>
        </div>
    );
}