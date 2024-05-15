import type { Load } from '@sveltejs/kit';

export const load: Load = async ({ fetch }) => {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/hackathons`);
    if (!res.ok) {
        throw new Error('Failed to fetch hackathons');
    }
    const hackathons = await res.json();
    return { hackathons };
};
