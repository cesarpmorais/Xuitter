"use client";

import { useState } from "react";
import { login } from "../api/backendApi";
import { useRouter } from "next/navigation";

export default function LoginForm() {
    const [email, set_email] = useState("");
    const [password, set_password] = useState("");
    const [loading, set_loading] = useState(false);
    const [error, set_error] = useState<string | null>(null);
    const [success, set_success] = useState(false);
    const router = useRouter();

    async function handle_submit(e: React.FormEvent) {
        e.preventDefault();
        set_loading(true);
        set_error(null);

        try {
            const response = await login({ email, password });
            localStorage.setItem("access_token", response.access);
            set_success(true);
            router.push("/");
        } catch (err) {
            set_error((err as Error).message);
        } finally {
            set_loading(false);
        }
    }

    if (success) {
        return <p>Login realizado com sucesso!</p>;
    }

    return (
        <form onSubmit={handle_submit} className="max-w-md mx-auto p-4 border rounded">
            <h2 className="text-2xl mb-4">Entrar</h2>
            <label>
                E-mail
                <input
                    type="text"
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
                {loading ? "Entrando..." : "Entrar"}
            </button>
            <button
                type="button"
                onClick={() => router.push("/signup")}
                className="ml-4 bg-gray-300 text-black py-2 px-4 rounded"
            >
                Criar conta
            </button>
        </form>
    );
}