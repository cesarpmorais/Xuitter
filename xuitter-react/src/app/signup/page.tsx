"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signup } from "../api/backendApi";


export default function SignupForm() {
    const router = useRouter();
    const [username, set_username] = useState("");
    const [email, set_email] = useState("");
    const [password, set_password] = useState("");
    const [loading, set_loading] = useState(false);
    const [error, set_error] = useState<string | null>(null);
    const [success, set_success] = useState(false);

    async function handle_submit(e: React.FormEvent) {
        e.preventDefault();
        set_loading(true);
        set_error(null);

        try {
            await signup({ username, email, password });
            set_success(true);
        } catch (err) {
            set_error((err as Error).message);
        } finally {
            set_loading(false);
        }
    }

    if (success) {
        router.push("/login");
    }

    return (
        <form onSubmit={handle_submit} className="max-w-md mx-auto p-4 border rounded">
            <h2 className="text-2xl mb-4">Criar conta</h2>
            <label>
                Username
                <input
                    type="text"
                    value={username}
                    onChange={e => set_username(e.target.value)}
                    className="block w-full border p-2 mb-3"
                    required
                />
            </label>
            <label>
                Email
                <input
                    type="email"
                    value={email}
                    onChange={e => set_email(e.target.value)}
                    className="block w-full border p-2 mb-3"
                    required
                />
            </label>
            <label>
                Senha
                <input
                    type="password"
                    value={password}
                    onChange={e => set_password(e.target.value)}
                    className="block w-full border p-2 mb-3"
                    required
                />
            </label>
            {error && <p className="text-red-600 mb-3">{error}</p>}
            <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 text-white py-2 px-4 rounded disabled:opacity-50"
            >
                {loading ? "Criando..." : "Criar Conta"}
            </button>
        </form>
    );
}
