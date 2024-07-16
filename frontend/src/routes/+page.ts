import type { Load } from '@sveltejs/kit';

export const load: Load = async ({ fetch }) => {
    try{
    const res = await fetch(`${import.meta.env.VITE_API_URL}/hackathons`);
    if (!res.ok) {
        throw new Error('Failed to fetch hackathons');
    }
    const hackathons = await res.json();
    return { hackathons };
    }
    catch (error) {
        return {
            hackathons: [],
            error: 'Failed to fetch hackathons. Please try again later.'
        };
    }
};
